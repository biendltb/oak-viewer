from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import mainthread


from oak_viewer.gui.setting_panel import SettingPanel
from oak_viewer.gui.content_panel import ContentPanel
from oak_viewer.gui.status_bar import StatusBar


class OakViewer(Widget):
    setting_panel = ObjectProperty(None)
    content_panel = ObjectProperty(None)
    status_bar = ObjectProperty(None)

    @mainthread
    def update_image(self, frame, cam_type):
        self.content_panel.update_image(frame, cam_type)


