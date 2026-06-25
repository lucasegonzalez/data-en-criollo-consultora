import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")
HERMES_API_KEY = os.getenv("HERMES_API_KEY", "change_me")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
