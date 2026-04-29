from app.database import SessionLocal
from app.models import NotificationTemplate, InfoSystem

def init_test_data():
    db = SessionLocal()
    try:
        # Проверяем, есть ли хотя бы один шаблон
        if not db.query(NotificationTemplate).first():
            # Создаём шаблон
            template = NotificationTemplate(
                name="welcome",
                title="Добро пожаловать",
                body="Тестовое сообщение для проверки API"
            )
            db.add(template)
            db.commit()
            db.refresh(template)
            
            # Создаём информационную систему
            info_system = InfoSystem(
                name="Моя тестовая система",
                template_id=template.id
            )
            db.add(info_system)
            db.commit()
            print("✅ Тестовые данные успешно добавлены")
        else:
            print("ℹ️ Тестовые данные уже существуют")
    except Exception as e:
        print(f"⚠️ Ошибка при добавлении тестовых данных: {e}")
    finally:
        db.close()