from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from enum import Enum


class OpenFileDialog(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)
    ok_btn_text = ObjectProperty('OK')
    cancel_btn_text = ObjectProperty('Cancel')
    # last_dir = ObjectProperty('')


class Notification(Popup):
    def __init__(self, **kwargs):
        super(Notification, self).__init__(**kwargs)


class MsgType(Enum):
    ERROR = 0
    WARNING = 1
    INFO = 2


def show_notification(msg_type, msg):
    noti_title = 'ERROR'
    msg_color = 'FF0000'
    if msg_type == MsgType.WARNING:
        noti_title = 'WARNING'
        msg_color = 'FFFF00'
    elif msg_type == MsgType.INFO:
        noti_title = 'INFO'
        msg_color = '7CFC00'

    error_popup = Notification(title=noti_title, size_hint=(None, None), size=(400, 200))
    error_popup.display_text = '[color=#{}]{}[/color]'.format(msg_color, msg)
    error_popup.open()