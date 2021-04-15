from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from oak_viewer.types import CameraType

class SettingPanel(GridLayout):
    def __init__(self, **kwargs):
        super(SettingPanel, self).__init__(**kwargs)

    def left_switch_change(self, is_active):
        print('Left mono change')
        app = App.get_running_app()
        if is_active:
            app.start_streaming(CameraType.LEFT)
        else:
            app.stop_streaming(CameraType.LEFT)

    def right_switch_change(self, is_active):
        print('Right mono change')
        app = App.get_running_app()
        if is_active:
            app.start_streaming(CameraType.RIGHT)
        else:
            app.stop_streaming(CameraType.RIGHT)

    def rgb_switch_change(self, is_active):
        print('Left mono change')
        app = App.get_running_app()
        if is_active:
            app.start_streaming(CameraType.RGB)
        else:
            app.stop_streaming(CameraType.RGB)

