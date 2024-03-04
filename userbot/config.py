import os

from dotenv import load_dotenv  # FOR ANDREW

load_dotenv()

TOKEN = os.getenv("TOKEN")
# TOKEN = os.getenv("USERTOKEN")
OWNER = int(os.getenv("OWNER"))
BACKEND_URL = os.getenv("BACKEND_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")

# ip = "cloud.scopevfx.ru"
# ip = "176.57.213.152"
ip = "sviat.online"
# ip = "89.108.98.124"
