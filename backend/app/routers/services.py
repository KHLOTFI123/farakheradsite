from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.i18n import normalize_lang, present
from app.models import Service, User
from app.schemas import ServiceIn, ServiceOut

public_router = APIRouter(prefix="/api/services", tags=["services"])
admin_router = APIRouter(prefix="/api/admin/services", tags=["admin-services"])


def _slug_taken(db: Session, slug: str, exclude_id: int | None = None) -> bool:
    query = db.query(Service).filter(Service.slug == slug)
    if exclude_id is not None:
        query = query.filter(Service.id != exclude_id)
    return query.first() is not None


@public_router.get("", response_model=list[ServiceOut])
def list_public_services(lang: str = "fa", db: Session = Depends(get_db)):
    rows = db.query(Service).order_by(Service.sort_order.asc(), Service.id.asc()).all()
    code = normalize_lang(lang)
    return [present("services", ServiceOut, row, code) for row in rows]


@public_router.get("/{slug}", response_model=ServiceOut)
def get_service(slug: str, lang: str = "fa", db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.slug == slug).first()
    if not service:
        raise HTTPException(status_code=404, detail="خدمت پیدا نشد")
    return present("services", ServiceOut, service, normalize_lang(lang))


@admin_router.get("", response_model=list[ServiceOut])
def list_services(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Service).order_by(Service.sort_order.asc(), Service.id.asc()).all()


@admin_router.post("", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceIn, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if _slug_taken(db, payload.slug):
        raise HTTPException(status_code=400, detail="این نامک قبلاً استفاده شده است")
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@admin_router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    payload: ServiceIn,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="خدمت پیدا نشد")
    if _slug_taken(db, payload.slug, exclude_id=service_id):
        raise HTTPException(status_code=400, detail="این نامک قبلاً استفاده شده است")
    for key, value in payload.model_dump().items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return service


@admin_router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="خدمت پیدا نشد")
    db.delete(service)
    db.commit()
