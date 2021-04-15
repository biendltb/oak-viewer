from kivy.uix.gridlayout import GridLayout
from kivy.graphics.texture import Texture

import numpy as np

from kivy.clock import Clock

from oak_viewer.types import CameraType


class ContentPanel(GridLayout):
    def __init__(self, **kwargs):
        super(ContentPanel, self).__init__(**kwargs)

        # run the update after the GUI is fully loaded
        Clock.schedule_once(lambda func: self._gui_value_init(), timeout=1.)

    def _gui_value_init(self):
        self.ids.im_left.source = ''
        self.ids.color = (0., 0., 0., 0.)
        self.ids.im_right.source = ''
        self.ids.im_rgb.source = ''

    def update_image(self, frame, cam_type):
        # convert image to 3 dimensions
        if len(frame.shape) == 2:
            frame = np.expand_dims(frame, axis=-1)

        display_im_ctl = self.ids.im_left
        c_format = 'luminance'

        if cam_type == CameraType.LEFT:
            display_im_ctl = self.ids.im_left
            c_format = 'luminance'
        elif cam_type == CameraType.RIGHT:
            display_im_ctl = self.ids.im_right
            c_format = 'luminance'
        elif cam_type == CameraType.RGB:
            display_im_ctl = self.ids.im_rgb
            c_format = 'bgr'

        im_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        im_texture.blit_buffer(np.flip(frame, axis=0).tobytes(), colorfmt=c_format, bufferfmt='ubyte')

        display_im_ctl.texture = im_texture
        display_im_ctl.reload()
        return True
