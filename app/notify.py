from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
def create_notification(request: NotifyRequest, db: Session = Depends(get_db)):
    template = db.query(NotificationTemplate).filter(NotificationTemplate.id == request.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    info_system = db.query(InfoSystem).filter(InfoSystem.id == request.information_system_id).first()
    if not info_system:
        raise HTTPException(status_code=404, detail="Info system not found")
    if request.transport not in ["vk", "max", "email"]:
        raise HTTPException(status_code=400, detail="Invalid transport")
    notification = Notification(
        template_id=request.template_id,
        information_system_id=request.information_system_id,
        user_mobile_phone=request.user_mobile_phone,
        user_email=request.user_email,
        transport=request.transport,
        status="pending"
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return {"status": "success", "notification_id": notification.id}