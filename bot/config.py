import os
from exceptions.no_available_ports import NoAvailablePorts
from utils.dbs.tokens import TokensDB

# from dotenv import load_dotenv  # FOR ANDREW
# import logging
#
# load_dotenv()

TOKEN = os.getenv("TOKEN")
OWNER = int(os.getenv("OWNER"))
BACKEND_URL = os.getenv("BACKEND_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")

# ip = "cloud.scopevfx.ru"
# ip = "176.57.213.152"
ip = "sviat.online"
# ip = "89.108.98.124"

# webhook settings
WEBHOOK_HOST = f"https://{ip}"
WEBHOOK_PORT = 443
# WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_PATH = f"/tblp"
# WEBHOOK_URL = f"{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


def get_webhook_url():
    used = TokensDB.get_used_ports()
    # logging.Logger.info(str(used))
    for port in range(7000, 8000):
        if not (port in used):
            return port, f"{WEBHOOK_HOST}:{port}"
    raise NoAvailablePorts


def get_webhook_path(token: str):
    return f"/tblp/{token}"


def get_webapp_host(token: str):
    return f"http://{WEBAPP_HOST}/tblp/{token}/webapp"


# webserver settings
WEBAPP_HOST = "0.0.0.0"
# WEBAPP_PORT = os.getenv("WEBAPP_PORT")
WEBAPP_PORT = ""
