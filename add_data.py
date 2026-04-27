import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import MobileUser, NotificationTemplate, InfoSystem

async def add_data():
    async with AsyncSessionLocal() as db:
        # 1. Добавляем мобильного пользователя
        new_user = MobileUser(
            phone_number="+79991112233",
            email="user@example.com",
            push_token="token123",
            is_active=True
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        print(f"Добавлен пользователь с id={new_user.id}")

        # 2. Добавляем шаблон уведомления
        new_template = NotificationTemplate(
            name="payment_reminder",
            title="Напоминание об оплате",
            body="Уважаемый пользователь, пожалуйста, оплатите счёт до 25 числа."
        )
        db.add(new_template)
        await db.commit()
        await db.refresh(new_template)
        print(f"Добавлен шаблон с id={new_template.id}")

        # 3. Добавляем информационную систему (связываем с шаблоном и пользователем)
        new_system = InfoSystem(
            name="Биллинг",
            description="Система учёта платежей",
            template_id=new_template.id,
            default_user_id=new_user.id,
            is_active=True
        )
        db.add(new_system)
        await db.commit()
        print(f"Добавлена инфосистема с id={new_system.id}")

asyncio.run(add_data())