from celery import Celery
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Notification

# Настройка Celery с RabbitMQ
celery_app = Celery(
    'notification_service',
    broker='amqp://guest:guest@rabbitmq:5672//',
    backend=None
)

# Получаем URL базы данных из окружения (такой же, как в приложении)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/notifications")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@celery_app.task(bind=True)
def process_notification(self, notification_id: int):
    """
    Заглушка: имитация отправки уведомления.
    Обновляет статус уведомления в БД.
    """
    db = SessionLocal()
    try:
        notification = db.query(Notification).get(notification_id)
        if not notification:
            return
        # Статус "в очереди"
        notification.status = "queued"
        db.commit()

        # Имитация обработки (например, задержка или просто лог)
        print(f"Обработка уведомления {notification_id}... (имитация)")

        # Статус "отправлено"
        notification.status = "sent"
        db.commit()
        print(f"Уведомление {notification_id} помечено как отправленное (заглушка).")
    except Exception as e:
        notification.status = "failed"
        db.commit()
        print(f"Ошибка при обработке уведомления {notification_id}: {e}")
    finally:
        db.close()