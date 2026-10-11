from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import settings
from app.database import get_db
from app.models import Message, User
from app.schemas import ContactIn, MessageOut
from app.security import rate_limit

public_router = APIRouter(prefix="/api/contact", tags=["contact"])
admin_router = APIRouter(prefix="/api/admin/messages", tags=["admin-messages"])


@public_router.post("", status_code=status.HTTP_201_CREATED)
def send_message(payload: ContactIn, request: Request, db: Session = Depends(get_db)):
    rate_limit(
        request,
        name="contact",
        limit=settings.contact_rate_limit,
        window_seconds=600,
    )
    data = payload.model_dump()
    data["name"] = data["name"].strip()
    data["phone"] = (data.get("phone") or "").strip()[:40]
    data["subject"] = (data.get("subject") or "").strip()[:200]
    data["body"] = data["body"].strip()[:5000]
    message = Message(**data)
    db.add(message)
    db.commit()
    return {"ok": True}


@admin_router.get("", response_model=list[MessageOut])
def list_messages(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Message).order_by(Message.created_at.desc()).all()


@admin_router.patch("/{message_id}/read", response_model=MessageOut)
def mark_read(message_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="پیام پیدا نشد")
    message.is_read = True
    db.commit()
    db.refresh(message)
    return message


@admin_router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="پیام پیدا نشد")
    db.delete(message)
    db.commit()
