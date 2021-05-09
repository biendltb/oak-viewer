import depthai as dai
from oak_viewer.types import CameraType

import logging
logger = logging.getLogger("spark_logging")


class OakDCamera:
    def __init__(self):
        self._q_left = None
        self._q_right = None
        self._q_rgb = None
        self._pipeline = dai.Pipeline()
        self._init_pipeline()

        self._is_started = False

    def _init_pipeline(self):
        """ Initialize the camera pipeline
        """
        # Define a source - two mono (grayscale) cameras
        cam_left = self._pipeline.createMonoCamera()
        cam_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        cam_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

        cam_right = self._pipeline.createMonoCamera()
        cam_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        cam_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

        cam_rgb = self._pipeline.createColorCamera()
        cam_rgb.setPreviewSize(640, 480)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

        # Create outputs
        xout_left = self._pipeline.createXLinkOut()
        xout_left.setStreamName('left')
        cam_left.out.link(xout_left.input)

        xout_right = self._pipeline.createXLinkOut()
        xout_right.setStreamName('right')
        cam_right.out.link(xout_right.input)

        xout_rgb = self._pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")
        cam_rgb.preview.link(xout_rgb.input)

        # check if the camera is available
        ret, _ = dai.Device.getAnyAvailableDevice()
        if ret is False:
            logger.fatal('No camera available.')
            exit(1)
        else:
            self._device = dai.Device(self._pipeline)
            logger.info('Camera device is connected.')

    def start(self):
        """ Start the pipeline
        """
        self._device.startPipeline()
        logger.info('Camera started.')
        # Output queues will be used to get the grayscale frames from the outputs defined above
        self._q_left = self._device.getOutputQueue(name="left", maxSize=4, blocking=True)
        self._q_right = self._device.getOutputQueue(name="right", maxSize=4, blocking=True)
        self._q_rgb = self._device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        self._is_started = True

    def grab(self, cam_type=CameraType.LEFT):
        """ Grab a frame from camera
            :param cam_type: which camera of the OAK-D cam
        """
        if cam_type == CameraType.LEFT:
            frame_q = self._q_left
        elif cam_type == CameraType.RIGHT:
            frame_q = self._q_right
        elif cam_type == CameraType.RGB:
            frame_q = self._q_rgb
        else:
            raise Exception('Type of camera is not supported')

        if frame_q is None:
            logger.error('Camera pipeline has not been started.')
            exit(1)

        in_frame = frame_q.get()
        return in_frame.getCvFrame()

    def stop(self):
        """ Close and stop the device
        """
        self._device.close()
