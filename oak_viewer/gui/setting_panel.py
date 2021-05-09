from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

from oak_viewer.types import CameraType
from oak_viewer.gui.recording_screen import RecordingScreen

import logging
logger = logging.getLogger("spark_logging")


class SettingPanel(GridLayout):
    def __init__(self, **kwargs):
        super(SettingPanel, self).__init__(**kwargs)
        self._main_screen = MainSettingScreen()
        self._main_screen.set_recording_callback(self._recording_press)

        self._recording_screen = RecordingScreen()
        self._recording_screen.set_back_btn_callback(self._back_btn_press)

        Clock.schedule_once(lambda func: self._init(), timeout=1.)

    def _init(self):
        self.ids.container.add_widget(self._main_screen)
        # self.ids.container.add_widget(self._recording_screen)

    def _recording_press(self):
        self.ids.container.remove_widget(self.ids.container.children[0])
        self.ids.container.add_widget(self._recording_screen)

    def _back_btn_press(self):
        self.ids.container.remove_widget(self.ids.container.children[0])
        self.ids.container.add_widget(self._main_screen)

    def switch_all_cams_off(self):
        """
        Switch all cameras off
        :return: None
        """
        logger.info('Switch all current streams off.')
        self._main_screen.ids.left_cam_switch.active = False
        self._main_screen.ids.right_cam_switch.active = False
        self._main_screen.ids.rgb_cam_switch.active = False

    def update_rec_timer(self, time_s):
        """ Update recording timer during recording
            :param time_s: time in seconds
        """
        self._recording_screen.update_rec_timer(time_s)


class MainSettingScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainSettingScreen, self).__init__(**kwargs)
        # on/off state map for cameras: left - rgb - right
        self._cam_layout = int('0b000', 2)
        self._recording_callback = None

    def set_recording_callback(self, callback):
        self._recording_callback = callback

    def left_switch_change(self, is_active):
        logger.debug('LEFT mono switch: {}'.format('ON' if is_active else 'OFF'))
        app = App.get_running_app()
        if is_active:
            self._cam_layout |= int('0b100', 2)
            app.start_streaming(CameraType.LEFT, self._cam_layout)
        else:
            self._cam_layout &= int('0b011', 2)
            app.stop_streaming(CameraType.LEFT, self._cam_layout)

    def right_switch_change(self, is_active):
        logger.debug('RIGHT mono switch: {}'.format('ON' if is_active else 'OFF'))
        app = App.get_running_app()
        if is_active:
            self._cam_layout |= int('0b001', 2)
            app.start_streaming(CameraType.RIGHT, self._cam_layout)
        else:
            self._cam_layout &= int('0b110', 2)
            app.stop_streaming(CameraType.RIGHT, self._cam_layout)

    def rgb_switch_change(self, is_active):
        logger.debug('RGB mono switch: {}'.format('ON' if is_active else 'OFF'))
        app = App.get_running_app()
        if is_active:
            self._cam_layout |= int('0b010', 2)
            app.start_streaming(CameraType.RGB, self._cam_layout)
        else:
            self._cam_layout &= int('0b101', 2)
            app.stop_streaming(CameraType.RGB, self._cam_layout)

    def recording_btn_press(self):
        # Add delay to show the effect
        self._recording_callback()


