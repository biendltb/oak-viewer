import time
import cv2

import logging
logger = logging.getLogger("spark_logging")


class Recorder:
    def __init__(self):
        self._video_path = None
        self._fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self._fps = 30
        self._resolution = None

        self._video_writer = None

        self._is_init = False
        self._is_first_write = True
        self._is_recording = False
        self._is_pause = False

    def _reset_recording(self):
        self._video_path = None
        self._resolution = None
        self._video_writer = None
        self._is_init = False
        self._is_first_write = True
        self._is_recording = False

    def init(self, video_path):
        """
        Initialize the recording with a saving directory.
        :param video_path:
        :return:
        """
        self._video_path = video_path
        self._is_init = True

    def write_frame(self, frame):
        """
        Write frame to the current recording
        :param frame:
        :return: bool
        """
        if self._is_init is False:
            logger.fatal('Recorder has not been initialized.')
            exit(1)

        if self._is_first_write:
            if frame is None:
                return False
            self._resolution = frame.shape[:2][::-1]
            # init the writer
            is_color = True
            if len(frame.shape) == 2 or frame.shape[-1] == 1:
                is_color = False
            self._video_writer = cv2.VideoWriter(self._video_path, self._fourcc, self._fps, self._resolution,
                                                 isColor=is_color)
            self._is_first_write = False

        self._video_writer.write(frame)
        return True

    def set_recording_status(self, status):
        self._is_recording = status

    def is_recording(self):
        return self._is_recording

    def close(self):
        self._video_writer.release()
        self._reset_recording()






