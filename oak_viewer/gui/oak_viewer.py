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
    def update_image(self, frame, cam_type, cam_layout):
        """
        Update images on the display
        :param frame:
        :param cam_type:
        :param cam_layout:
        :return:
        """
        self.content_panel.update_image(frame, cam_type, cam_layout)

    @mainthread
    def switch_all_cams_off(self):
        """
        Switch all cam off from GUI
        :return: None
        """
        self.setting_panel.switch_all_cams_off()

    @mainthread
    def update_rec_timer(self, time_s):
        self.setting_panel.update_rec_timer(time_s)


