import configparser
import logging

PYHWA_VERSION = "1.3-beta"


# ? load pyhwa.ini
config = configparser.ConfigParser()
config.read("pyhwa.ini")
# DATA_PATH = "static/content"
DATA_PATH = config["path"]["DATA_PATH"]
# DATA_PATH_META = "static/meta"
DATA_PATH_META = config["path"]["meta_path"]
# PYHWA_PORT = 5113
# PYHWA_PORT = 5000
PYHWA_PORT = config["server"]["port"]
# PYHWA_LOCAL_NETWORK = True
PYHWA_LOCAL_NETWORK = config.getboolean("server", "allow_local_network")
EN_LOGS = config.getboolean("logs", "logs_enable")
LVL_LOGS = config.get("logs", "logs_level")
AUTO_META_SOURCE = config.get("server", "auto_meta_source")

# ? logging
logger = logging.getLogger("pyhwa")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("pyhwa.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


# ? show settings
allConfig = [
    {
        "data_path": DATA_PATH,
        "data_path_meta": DATA_PATH_META,
        "port": PYHWA_PORT,
        "local_network": PYHWA_LOCAL_NETWORK,
        "enable_logs": EN_LOGS,
        "logs_level": LVL_LOGS,
    }
]

def logWriter(msg, lvl="debug"):
    if EN_LOGS:
        if lvl == "debug":
            logger.debug(msg)
        if lvl == "info":
            logger.info(msg)
        if lvl == "warning":
            logger.warning(msg)
        if lvl == "error":
            logger.error(msg)
        return True
    else:
        return False
    
logWriter("var preview " + str(allConfig))