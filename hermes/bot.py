import logging
import time

from config import TELEGRAM_TOKEN, WHATSAPP_TOKEN
from api_client import health, get_pending_tasks, get_upcoming_meetings, create_task
from scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("🐍 Hermes AI Agent starting...")
    
    # Verify connection to FastAPI
    try:
        h = health()
        logger.info(f"✅ FastAPI connection OK: {h}")
    except Exception as e:
        logger.error(f"❌ FastAPI connection failed: {e}")
        logger.info("Hermes will keep trying...")
    
    # Start the proactive scheduler
    scheduler = start_scheduler()
    
    # Placeholder for Telegram bot
    if TELEGRAM_TOKEN:
        logger.info("Telegram token configured — bot ready (awaiting implementation)")
    
    # Placeholder for WhatsApp bot
    if WHATSAPP_TOKEN:
        logger.info("WhatsApp token configured — bot ready (awaiting implementation)")
    
    # CLI mode: respond to direct commands (used by user in terminal)
    logger.info("Hermes is running. Commands: health, tasks, meetings, create-task <title>")
    
    try:
        while True:
            cmd = input("hermes> ").strip()
            if cmd == "health":
                print(health())
            elif cmd == "tasks":
                tasks = get_pending_tasks()
                for t in tasks:
                    print(f"  [{t['estado']}] {t['titulo']} - {t.get('deadline', 'sin fecha')[:10]}")
            elif cmd == "meetings":
                meetings = get_upcoming_meetings()
                for m in meetings:
                    print(f"  {m['fecha'][:16]} - {m.get('notas', 'Sin título')}")
            elif cmd.startswith("create-task"):
                _, *parts = cmd.split(maxsplit=1)
                if parts:
                    result = create_task(parts[0])
                    print(f"✅ Tarea creada: {result}")
                else:
                    print("❌ Usá: create-task <título>")
            elif cmd in ("exit", "quit"):
                break
            else:
                print("Comandos: health, tasks, meetings, create-task <title>, exit")
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        scheduler.shutdown()
        logger.info("Hermes stopped.")

if __name__ == "__main__":
    main()
