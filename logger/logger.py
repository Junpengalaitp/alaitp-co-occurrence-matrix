import logging.config
import os
import platform

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_path = os.path.join(BASE_DIR, 'config', 'logging.yaml')


def init_dir(env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            _dict = yaml.load(f)
            handlers = _dict['handlers']
            for key in handlers:
                handler = handlers[key]
                handler.setdefault('filename', None)
                log_path = handler['filename']
                if log_path is not None:
                    system = platform.system()
                    if not os.path.exists(log_path):
                        dir_path = os.path.split(log_path)
                        if 'Windows' == system:
                            # os.path.sep
                            if not os.path.exists(dir_path[0]):
                                os.mkdir(dir_path[0])
                            # os.mkdir(dir_path[0] + os.path.sep + dir_path[1])
                            open(log_path, 'w+').close()
                        if 'Linux' == system:
                            # os.path.altsep
                            if not os.path.exists(dir_path[0]):
                                os.mkdir(dir_path[0])
                                os.mknod(dir_path[0])


def setup_logging(default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            logging.config.dictConfig(yaml.load(f))
    else:
        logging.basicConfig(level=default_level)


init_dir()
setup_logging()
logger = logging.getLogger("fileLogger")
