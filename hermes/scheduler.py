import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from api_client import get_pending_tasks, get_upcoming_meetings

logger = logging.getLogger(__name__)

def check_pending_tasks():
    """Check for overdue tasks and alert"""
    tasks = get_pending_tasks()
    now = datetime.utcnow()
    overdue = [t for t in tasks if t.get("deadline") and datetime.fromisoformat(t["deadline"]) < now]
    if overdue:
        msg = f"⚠️ Tenés {len(overdue)} tareas vencidas:\n"
        for t in overdue[:5]:
            msg += f"  • {t['titulo']} (deadline: {t['deadline'][:10]})\n"
        logger.warning(msg)
    else:
        logger.info(f"✅ {len(tasks)} tareas pendientes, ninguna vencida")

def check_upcoming_meetings():
    """Check for meetings in the next hour"""
    from datetime import timedelta
    now = datetime.utcnow()
    soon = now + timedelta(hours=1)
    meetings = get_upcoming_meetings()
    for m in meetings:
        meeting_time = datetime.fromisoformat(m["fecha"])
        if now <= meeting_time <= soon:
            logger.info(f"🔔 Recordatorio: Reunión en 1 hora - {m.get('notas', 'Sin título')}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_pending_tasks, "interval", minutes=15, id="check_tasks")
    scheduler.add_job(check_upcoming_meetings, "interval", minutes=5, id="check_meetings")
    scheduler.start()
    logger.info("Hermes scheduler started — checking every 15min for tasks, 5min for meetings")
    return scheduler
