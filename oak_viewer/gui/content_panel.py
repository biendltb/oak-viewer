from kivy.uix.gridlayout import GridLayout
from kivy.graphics.texture import Texture

import numpy as np

from kivy.clock import Clock

from oak_viewer.types import CameraType

import logging
logger = logging.getLogger("spark_logging")


class ImageLayout3(GridLayout):
    def __init__(self, **kwargs):
        super(ImageLayout3, self).__init__(**kwargs)


class ImageLayout2(GridLayout):
    def __init__(self, **kwargs):
        super(ImageLayout2, self).__init__(**kwargs)


class ImageLayout1(GridLayout):
    def __init__(self, **kwargs):
        super(ImageLayout1, self).__init__(**kwargs)


class ContentPanel(GridLayout):
    def __init__(self, **kwargs):
        super(ContentPanel, self).__init__(**kwargs)

        # initial layout: 0
        self._curr_n_active_cam = 0
        self._layout3 = ImageLayout3()
        self._layout2 = ImageLayout2()
        self._layout1 = ImageLayout1()

        # run the update after the GUI is fully loaded
        Clock.schedule_once(lambda func: self._gui_value_init(), timeout=1.)

        # must pass a function, not just a callback to make it work
        # Clock.schedule_once(lambda func: self.test_add_widget(), timeout=1.)
        # Clock.schedule_once(lambda func: self.test_remove_widget(), timeout=3.)

    def _gui_value_init(self):
        self._layout3.ids.im_l30.source = ''
        self._layout3.ids.im_l31.source = ''
        self._layout3.ids.im_l32.source = ''
        self._layout2.ids.im_l20.source = ''
        self._layout2.ids.im_l21.source = ''
        self._layout1.ids.im_l10.source = ''
        self.ids.color = (0., 0., 0., 0.)

    def update_image(self, frame, cam_type, cam_layout):
        # check layout number by counting how many cameras/bits on
        n_active_cam = bin(cam_layout).count('1')

        if n_active_cam == 0:
            return False

        if self._curr_n_active_cam != n_active_cam:
            self._update_layout(target_layout=n_active_cam)
            self._curr_n_active_cam = n_active_cam

        # convert image to 3 dimensions
        if len(frame.shape) == 2:
            frame = np.expand_dims(frame, axis=-1)

        display_im_ctl = None
        c_format = 'luminance'

        # if only one camera is on, there is only one choice for the display control
        if self._curr_n_active_cam == 1:
            display_im_ctl = self._layout1.ids.im_l10

        if cam_type == CameraType.LEFT:
            c_format = 'luminance'
            # left is always in the left image in the case of 2 or 3 cams
            if self._curr_n_active_cam == 2:
                display_im_ctl = self._layout2.ids.im_l20
            elif self._curr_n_active_cam == 3:
                display_im_ctl = self._layout3.ids.im_l30

        elif cam_type == CameraType.RIGHT:
            c_format = 'luminance'
            if self._curr_n_active_cam == 2:
                # right would be right if Left cam presents and left if RGB cam presents
                if cam_layout & int('0b100', 2) > 0:
                    display_im_ctl = self._layout2.ids.im_l21
                elif cam_layout & int('0b010', 2) > 0:
                    display_im_ctl = self._layout2.ids.im_l20
            elif self._curr_n_active_cam == 3:
                display_im_ctl = self._layout3.ids.im_l31

        elif cam_type == CameraType.RGB:
            c_format = 'bgr'
            # RGB image is always in the left
            if self._curr_n_active_cam == 2:
                display_im_ctl = self._layout2.ids.im_l21
            elif self._curr_n_active_cam == 3:
                display_im_ctl = self._layout3.ids.im_l32

        if display_im_ctl is None:
            logger.error('ERROR: No display control matches with the layout: {0:03b}'.format(cam_layout))
            return False

        im_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        im_texture.blit_buffer(np.flip(frame, axis=0).tobytes(), colorfmt=c_format, bufferfmt='ubyte')

        display_im_ctl.texture = im_texture
        display_im_ctl.reload()
        return True

    def _update_layout(self, target_layout):
        assert 0 <= target_layout <= 3, 'ERROR: Target layout is out of valid range.'

        # remove old layout
        if len(self.ids.image_layout.children) > 0:
            self.ids.image_layout.remove_widget(self.ids.image_layout.children[0])

        # add layout
        if target_layout == 3:
            self.ids.image_layout.add_widget(self._layout3)
        elif target_layout == 2:
            self.ids.image_layout.add_widget(self._layout2)
        elif target_layout == 1:
            self.ids.image_layout.add_widget(self._layout1)
