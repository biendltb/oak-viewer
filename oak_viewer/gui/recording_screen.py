import time

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup

from oak_viewer.gui.dialogs import OpenFileDialog, show_notification, MsgType
from oak_viewer.types import CameraType
from oak_viewer.utils import format_time_str

import logging
logger = logging.getLogger("spark_logging")


class RecordingScreen(GridLayout):
    def __init__(self, **kwargs):
        super(RecordingScreen, self).__init__(**kwargs)
        self._start_section = RecordingStartSection()
        self._start_section.set_start_btn_callback(self.start_btn_press)

        self._stop_section = RecordingStopSection()
        self._stop_section.set_pause_btn_callback(self.pause_btn_press)
        self._stop_section.set_stop_btn_callback(self.stop_btn_press)

        self._back_btn_callback = None

        self._popup = None

        Clock.schedule_once(lambda func: self._init(), timeout=1.)

    def _init(self):
        self.ids.lower_section.add_widget(self._start_section)

    def set_back_btn_callback(self, callback):
        self._back_btn_callback = callback

    def back_btn_press(self):
        logger.debug('Back to main screen.')
        if self._back_btn_callback is None:
            logger.error('Callback for back button is not set yet.')
            return
        self._back_btn_callback()
        # Clock.schedule_once(lambda func: self._back_btn_callback(), timeout=.5)

    def start_btn_press(self):
        """ Start recording button press
            Get camera type, saving directory and video path prefix before start the recording
        """
        video_name_prefix = 'record_cam_'
        curr_btn_text = self.ids.camera_type_btn.text
        cam_type = None
        if curr_btn_text == 'LEFT camera':
            cam_type = CameraType.LEFT
            video_name_prefix += 'left_'
        elif curr_btn_text == 'RIGHT camera':
            cam_type = CameraType.RIGHT
            video_name_prefix += 'right_'
        elif curr_btn_text == 'RGB camera':
            cam_type = CameraType.RGB
            video_name_prefix += 'rgb_'
        else:
            logger.fatal('Camera type is not supported.')
            exit(1)

        saving_dir = self.ids.saving_dir_textbox.text
        if saving_dir == '':
            msg = 'Recording saving path has not been specified.'
            logger.error(msg)
            show_notification(MsgType.ERROR, msg)
            return

        video_name_prefix += '{}'.format(int(time.time()))

        app = App.get_running_app()
        app.start_recording(cam_type, saving_dir, video_name_prefix)

        self.ids.lower_section.remove_widget(self.ids.lower_section.children[0])
        self.ids.lower_section.add_widget(self._stop_section)

    def pause_btn_press(self, is_paused):
        """ Pause/Resume button press
        """
        app = App.get_running_app()
        app.pause_and_resume(is_paused)

    def stop_btn_press(self):
        app = App.get_running_app()
        app.stop_recording()

        self.ids.lower_section.remove_widget(self.ids.lower_section.children[0])
        self.ids.lower_section.add_widget(self._start_section)

    def saving_dir_btn_press(self):
        content = OpenFileDialog(select=self._dir_select_ok,
                                 cancel=self._dir_select_cancel,
                                 ok_btn_text='OK')
        self._popup = Popup(title='Select saving dir', content=content, size_hint=(0.9, 0.9))
        Clock.schedule_once(lambda func: self._popup.open(), timeout=.2)

    def _dir_select_ok(self, selected_dir, file_paths):
        self.ids.saving_dir_textbox.text = selected_dir
        self._popup.dismiss()

    def _dir_select_cancel(self):
        self._popup.dismiss()

    def update_rec_timer(self, time_s):
        """ Update recording timer during recording
            :param time_s: time in seconds
        """
        self._stop_section.ids.rec_time_lbl.text = format_time_str(int(round(time_s)))


class RecordingStartSection(GridLayout):
    def __init__(self, **kwargs):
        super(RecordingStartSection, self).__init__(**kwargs)
        self._start_btn_press_callback = None

    def set_start_btn_callback(self, callback):
        self._start_btn_press_callback = callback

    def start_btn_press(self):
        if self._start_btn_press_callback is not None:
            self._start_btn_press_callback()


class RecordingStopSection(GridLayout):
    def __init__(self, **kwargs):
        super(RecordingStopSection, self).__init__(**kwargs)
        self._pause_btn_callback = None
        self._stop_btn_callback = None

        # TODO: use config file to store icon path
        self._pause_icon_path = 'oak_viewer/gui/ims/outline_pause_circle_white_24dp.png'
        self._resume_icon_path = 'oak_viewer/gui/ims/outline_resume_circle_white_24dp.png'

        # the recording is not paused by default
        self._is_paused = False

    def set_pause_btn_callback(self, callback):
        self._pause_btn_callback = callback

    def set_stop_btn_callback(self, callback):
        self._stop_btn_callback = callback

    def pause_btn_press(self):
        if self._pause_btn_callback is None:
            logger.error('Pause callback has not been assigned.')
            return

        self._is_paused = not self._is_paused

        if self._is_paused is True:
            # change to resume display
            self.ids.pause_icon_im.source = self._resume_icon_path
        else:
            self.ids.pause_icon_im.source = self._pause_icon_path

        self._pause_btn_callback(self._is_paused)

    def stop_btn_press(self):
        if self._stop_btn_callback is not None:
            self._stop_btn_callback()
