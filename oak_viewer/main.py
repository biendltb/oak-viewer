from oak_viewer.oak_viewer_app import OakViewerApp
from oak_viewer.oak_logging import setup_logging


if __name__ == '__main__':
    setup_logging()
    OakViewerApp().run()
