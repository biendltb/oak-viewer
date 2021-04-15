import time

import kivy
kivy.require('2.0.0')

import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
Builder.load_file('gui/oak_viewer.kv')

from oak_viewer.gui.oak_viewer import OakViewer
from oak_viewer.oak_d_cam import OakDCamera
from oak_viewer.types import CameraType


class OakViewerApp(App):
    def __init__(self, **kwargs):
        super(OakViewerApp, self).__init__(**kwargs)
        self._main_window = None
        self._oak_d_cam = OakDCamera()
        self._oak_d_cam.start()

        self._is_left_streaming = False
        self._is_right_streaming = False
        self._is_rgb_streaming = False

    def build(self):
        self.title = 'OAK Viewer'
        Window.minimum_height = 800
        Window.minimum_width = 1200
        Window.bind(on_request_close=self.on_request_close)
        self._main_window = OakViewer()
        return self._main_window

    def start_streaming(self, cam_type):
        if cam_type == CameraType.LEFT:
            self._is_left_streaming = True
        elif cam_type == CameraType.RIGHT:
            self._is_right_streaming = True
        elif cam_type == CameraType.RGB:
            self._is_rgb_streaming = True

        print('Streaming start.')
        # start a thread for streaming
        stream_thread = threading.Thread(target=self._streaming_task, args=(cam_type,))
        stream_thread.start()

    def _streaming_task(self, cam_type):
        if cam_type == CameraType.LEFT:
            while self._is_left_streaming:
                frame = self._oak_d_cam.grab(cam_type=cam_type)
                self._main_window.update_image(frame, cam_type=cam_type)
        elif cam_type == CameraType.RIGHT:
            while self._is_right_streaming:
                frame = self._oak_d_cam.grab(cam_type=cam_type)
                self._main_window.update_image(frame, cam_type=cam_type)
        elif cam_type == CameraType.RGB:
            while self._is_rgb_streaming:
                frame = self._oak_d_cam.grab(cam_type=cam_type)
                self._main_window.update_image(frame, cam_type=cam_type)

    def stop_streaming(self, cam_type):
        if cam_type == CameraType.LEFT:
            self._is_left_streaming = False
        elif cam_type == CameraType.RIGHT:
            self._is_right_streaming = False
        elif cam_type == CameraType.RGB:
            self._is_rgb_streaming = False

        print('Streaming stop.')

    def on_request_close(self, *args):
        # Ensure that all streaming threads are stop
        self.stop_streaming(CameraType.LEFT)
        self.stop_streaming(CameraType.RIGHT)
        self.stop_streaming(CameraType.RGB)

        # wait for threads exit
        time.sleep(0.5)
        print('App closing...')
