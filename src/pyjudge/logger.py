from .config import read_global_config
from datetime import datetime

COLORMAP = {
    "info": "\033[0m",
    "warning": "\033[93m",
    "error": "\033[91m",
    "success": "\033[92m",
    "debug": "\033[95m",
    "remind": "\033[94m",
}
HEADER_FORMAT = "[%s][%s][%s]"

config = read_global_config()

class Logger:
    def __init__(self, name="UNKNOWN"):
        self.name = name
    def log(self, *msg, level="info", glue=" ", debug:bool=False) -> None:
        if debug and not config['debug']:
            return
        msgl = []
        for item in msg:
            msgl.append(str(item))
        msgline = HEADER_FORMAT % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.name, level.upper()) + glue.join(msgl)
        print(COLORMAP[level.lower()]+msgline+COLORMAP["info"])
    def info(self, *msg, debug=False):
        self.log(*msg, level="info", debug=debug)
    def warn(self, *msg, debug=False):
        self.log(*msg, level="warning", debug=debug)
    def error(self, *msg, debug=False):
        self.log(*msg, level="error", debug=debug)
    def success(self, *msg, debug=False):
        self.log(*msg, level="success", debug=debug)
    def debug(self, *msg):
        if config['debug']:
            self.log(*msg, level="debug")
    def remind(self, *msg, debug=False):
        self.log(*msg, level="remind", debug=debug)