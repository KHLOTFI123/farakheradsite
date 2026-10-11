from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.i18n import normalize_lang, present
from app.models import Slide, User
from app.schemas import SlideIn, SlideOut

public_router = APIRouter(prefix="/api/slides", tags=["slides"])
admin_router = APIRouter(prefix="/api/admin/slides", tags=["admin-slides"])


@public_router.get("", response_model=list[SlideOut])
def list_public_slides(lang: str = "fa", db: Session = Depends(get_db)):
    rows = (
        db.query(Slide)
        .filter(Slide.is_active.is_(True))
        .order_by(Slide.sort_order.asc(), Slide.id.asc())
        .all()
    )
    code = normalize_lang(lang)
    return [present("slides", SlideOut, row, code) for row in rows]


@admin_router.get("", response_model=list[SlideOut])
def list_slides(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Slide).order_by(Slide.sort_order.asc(), Slide.id.asc()).all()


@admin_router.post("", response_model=SlideOut, status_code=status.HTTP_201_CREATED)
def create_slide(payload: SlideIn, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    slide = Slide(**payload.model_dump())
    db.add(slide)
    db.commit()
    db.refresh(slide)
    return slide


@admin_router.put("/{slide_id}", response_model=SlideOut)
def update_slide(
    slide_id: int,
    payload: SlideIn,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    slide = db.get(Slide, slide_id)
    if not slide:
        raise HTTPException(status_code=404, detail="اسلاید پیدا نشد")
    for key, value in payload.model_dump().items():
        setattr(slide, key, value)
    db.commit()
    db.refresh(slide)
    return slide


@admin_router.delete("/{slide_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slide(slide_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    slide = db.get(Slide, slide_id)
    if not slide:
        raise HTTPException(status_code=404, detail="اسلاید پیدا نشد")
    db.delete(slide)
    db.commit()
