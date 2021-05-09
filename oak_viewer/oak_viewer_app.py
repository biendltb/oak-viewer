import kivy
kivy.require('2.0.0')


import time
import threading
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
Builder.load_file('gui/oak_viewer.kv')

from oak_viewer.gui.oak_viewer import OakViewer
from oak_viewer.oak_d_cam import OakDCamera
from oak_viewer.types import CameraType
from oak_viewer.recording import Recorder

import logging
logger = logging.getLogger("spark_logging")


class OakViewerApp(App):
    def __init__(self, **kwargs):
        super(OakViewerApp, self).__init__(**kwargs)
        self._main_window = None
        self._oak_d_cam = OakDCamera()
        self._oak_d_cam.start()

        self._is_left_streaming = False
        self._is_right_streaming = False
        self._is_rgb_streaming = False

        # identify the ON/OFF state of each camera
        self._curr_cam_layout = int('0b000', 2)

        self._recorder = None
        self._recording_thread = None
        self._is_recording_paused = False
        self._rec_prev_frame_time = None
        self._total_rec_time = 0

    def build(self):
        self.title = 'OAK Viewer'
        Window.minimum_height = 700
        Window.minimum_width = 1300
        Window.bind(on_request_close=self.on_request_close)
        self._main_window = OakViewer()
        return self._main_window

    def start_streaming(self, cam_type, cam_layout):
        self._curr_cam_layout = cam_layout

        if cam_type == CameraType.LEFT:
            logger.info('Left cam stream started.')
            self._is_left_streaming = True
        elif cam_type == CameraType.RIGHT:
            logger.info('Right cam stream started.')
            self._is_right_streaming = True
        elif cam_type == CameraType.RGB:
            logger.info('RGB cam stream started.')
            self._is_rgb_streaming = True

        # start a thread for streaming
        stream_thread = threading.Thread(target=self._streaming_task, args=(cam_type,))
        stream_thread.start()

    def _streaming_task(self, cam_type):
        frame = None
        if cam_type == CameraType.LEFT:
            while self._is_left_streaming:
                frame = self._oak_d_cam.grab(cam_type=cam_type)
                self._main_window.update_image(frame, cam_type, self._curr_cam_layout)
        elif cam_type == CameraType.RIGHT:
            while self._is_right_streaming:
                frame = self._oak_d_cam.grab(cam_type=cam_type)
                self._main_window.update_image(frame, cam_type, self._curr_cam_layout)
        elif cam_type == CameraType.RGB:
            while self._is_rgb_streaming:
                frame = self._oak_d_cam.grab(cam_type=cam_type)
                self._main_window.update_image(frame, cam_type, self._curr_cam_layout)

    def stop_streaming(self, cam_type, cam_layout):
        self._curr_cam_layout = cam_layout
        if cam_type == CameraType.LEFT and self._is_left_streaming:
            logger.info('Left cam stream was stopped.')
            self._is_left_streaming = False
        elif cam_type == CameraType.RIGHT and self._is_right_streaming:
            logger.info('Right cam stream was stopped.')
            self._is_right_streaming = False
        elif cam_type == CameraType.RGB and self._is_rgb_streaming:
            logger.info('RGB cam stream was stopped.')
            self._is_rgb_streaming = False

    def start_recording(self, cam_type, saving_dir, video_name_prefix):
        """ Start the recording
            1. Switch off all current stream
            2. Keep layout as single cam layout
            3. Specify the video path
            4.
        """
        # switch off all current streams and set to single layout
        self._main_window.switch_all_cams_off()

        # construct the video path
        video_name = '{}.mp4'.format(video_name_prefix)
        video_path = os.path.join(saving_dir, video_name)

        # start a recording thread
        logger.info('Recording starting...')
        self._recorder = Recorder()
        self._recorder.init(video_path)
        self._recorder.set_recording_status(True)
        self._recording_thread = threading.Thread(target=self._recording_task, args=(cam_type,))
        self._recording_thread.start()

    def _recording_task(self, cam_type):
        self._rec_prev_frame_time = time.time()
        while self._recorder.is_recording():
            if not self._is_recording_paused:
                frame = self._oak_d_cam.grab(cam_type)
                self._recorder.write_frame(frame)

                self._total_rec_time += time.time() - self._rec_prev_frame_time
                self._main_window.update_rec_timer(self._total_rec_time)
                self._main_window.update_image(frame, cam_type, cam_layout=int('0b100', 2))
            else:
                time.sleep(0.1)

            self._rec_prev_frame_time = time.time()

    def pause_and_resume(self, is_paused):
        self._is_recording_paused = is_paused

    def stop_recording(self):
        logger.info('Stop recording...')
        self._recorder.set_recording_status(False)
        self._recording_thread.join()
        self._recorder.close()

        self._recorder = None
        self._recording_thread = None
        self._is_recording_paused = False
        self._rec_prev_frame_time = None
        self._total_rec_time = 0

    def on_request_close(self, *args):
        # Make that all streaming threads are stopped
        self.stop_streaming(CameraType.LEFT, self._curr_cam_layout)
        self.stop_streaming(CameraType.RIGHT, self._curr_cam_layout)
        self.stop_streaming(CameraType.RGB, self._curr_cam_layout)

        # wait for threads exit
        logger.info('App closing...')
