import os
import yaml
import logging.config
import logging


def setup_logging():
    path = 'oak_viewer/data/logging.yaml'
    env_key = 'OAK_LOG_CFG'
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                setup_default_logging(path)
    else:
        setup_default_logging(path)
        print('Failed to load configuration file. Using default configs')


def setup_default_logging(file_path):
    # Configure log file
    logging.basicConfig(filename=file_path, level=logging.DEBUG,
                        format='[%(filename)s:%(lineno)s - %(funcName)20s()][%(asctime)s][%(levelname)s] %(message)s')
