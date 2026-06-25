import requests
from config import FASTAPI_URL, HERMES_API_KEY

HEADERS = {"Authorization": f"Bearer {HERMES_API_KEY}"}

def health():
    r = requests.get(f"{FASTAPI_URL}/api/v1/health", timeout=5)
    return r.json()

def get_pending_tasks():
    r = requests.get(
        f"{FASTAPI_URL}/api/v1/tasks",
        params={"estado": "pending"},
        headers=HEADERS,
        timeout=5,
    )
    return r.json()

def get_upcoming_meetings(days=1):
    """Get meetings for the next N days"""
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    end = now + timedelta(days=days)
    r = requests.get(
        f"{FASTAPI_URL}/api/v1/meetings",
        headers=HEADERS,
        timeout=5,
    )
    meetings = r.json()
    # Filter on client side for simplicity
    return [m for m in meetings if now <= datetime.fromisoformat(m["fecha"]) <= end]

def create_task(titulo: str, descripcion: str = ""):
    r = requests.post(
        f"{FASTAPI_URL}/api/v1/tasks",
        json={"titulo": titulo, "descripcion": descripcion},
        headers=HEADERS,
        timeout=5,
    )
    return r.json()
