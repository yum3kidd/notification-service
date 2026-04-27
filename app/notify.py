from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
from app.database import get_db
from app.models import Notification, NotificationTemplate, InfoSystem

router = APIRouter(prefix="/api", tags=["notifications"])

class NotifyRequest(BaseModel):
    template_id: int
    information_system_id: int
    user_mobile_phone: str = Field(..., pattern=r'^\+?[0-9]{10,15}$')
    user_email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    transport: str

@router.post("/notify")
async def create_notification(request: NotifyRequest, db: AsyncSession = Depends(get_db)):
    # Проверяем шаблон
    result = await db.execute(select(NotificationTemplate).where(NotificationTemplate.id == request.template_id))
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Проверяем инфосистему
    result = await db.execute(select(InfoSystem).where(InfoSystem.id == request.information_system_id))
    info_system = result.scalar_one_or_none()
    if not info_system:
        raise HTTPException(status_code=404, detail="Info system not found")
    
    # Проверяем транспорт
    if request.transport not in ["vk", "max", "email"]:
        raise HTTPException(status_code=400, detail="Invalid transport")
    
    # Создаём уведомление
    notification = Notification(
        template_id=request.template_id,
        information_system_id=request.information_system_id,
        user_mobile_phone=request.user_mobile_phone,
        user_email=request.user_email,
        transport=request.transport,
        status="pending"
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    
    return {"status": "success", "notification_id": notification.id}