import configparser
import logging
import json

# ! Never change these values.
PYHWA_VERSION = "1.5-beta"
PYHWA_LICENSE = "GNU AGPL v3.0"
PYHWA_REPO = "https://github.com/kerogs/pyhwa"


# ? load pyhwa.ini
config = configparser.ConfigParser()

with open("pyhwa.ini", "r", encoding="utf-8") as configfile:
    config.read_file(configfile)
    
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
AUTO_META_SOURCE = config.get("metadata", "auto_meta_source") 
INDEX_AUTOMETA = config.getboolean("metadata", "index_autometa")
SERVER_REQUIRES_LOGIN = config.getboolean("security", "server_requires_login")
ADMIN_REQUIRES_LOGIN = config.getboolean("security", "admin_requires_login")

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

# ? all settings
allConfig = {
    "version": PYHWA_VERSION,
    "license": PYHWA_LICENSE, 
    "repo": PYHWA_REPO,
    
    "attributes": {
        
        "server_configuration": {
            "port": PYHWA_PORT,
            "local_network": PYHWA_LOCAL_NETWORK,
        },
        
        "metadata_configuration": {"auto_meta_source": AUTO_META_SOURCE},
        
        "data_paths": {
            "data_path": DATA_PATH,
            "data_path_meta": DATA_PATH_META,
        },
        
        "logs": {
            "enable_logs": EN_LOGS,
            "logs_level": LVL_LOGS,
        },
        
    }
}

# ? write settings
statusPath = "static/json/server_status.json"
with open(statusPath, "w") as f:
    json.dump(allConfig, f, indent=4)

# ? logs 
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


# logWriter("var preview " + str(allConfig))
