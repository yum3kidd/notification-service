from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class MobileUser(Base):
    __tablename__ = "mobile_users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    push_token = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    info_systems = relationship("InfoSystem", back_populates="default_user")

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    info_systems = relationship("InfoSystem", back_populates="template")
    notifications = relationship("Notification", back_populates="template")

class InfoSystem(Base):
    __tablename__ = "info_systems"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    template_id = Column(Integer, ForeignKey("notification_templates.id"), nullable=True)
    default_user_id = Column(Integer, ForeignKey("mobile_users.id"), nullable=True)
    template = relationship("NotificationTemplate", back_populates="info_systems")
    default_user = relationship("MobileUser", back_populates="info_systems")
    notifications = relationship("Notification", back_populates="info_system")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("notification_templates.id"), nullable=False)
    information_system_id = Column(Integer, ForeignKey("info_systems.id"), nullable=False)
    user_mobile_phone = Column(String(20), nullable=False)
    user_email = Column(String(100), nullable=True)
    transport = Column(String(20), nullable=False)  # 'vk', 'max', 'email'
    status = Column(String(20), default="pending")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    template = relationship("NotificationTemplate", back_populates="notifications")
    info_system = relationship("InfoSystem", back_populates="notifications")