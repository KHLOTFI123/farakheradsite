from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.i18n import normalize_lang, present
from app.models import Product, User
from app.schemas import ProductIn, ProductOut

public_router = APIRouter(prefix="/api/products", tags=["products"])
admin_router = APIRouter(prefix="/api/admin/products", tags=["admin-products"])


@public_router.get("", response_model=list[ProductOut])
def list_public_products(lang: str = "fa", db: Session = Depends(get_db)):
    rows = (
        db.query(Product)
        .filter(Product.is_active.is_(True))
        .order_by(Product.sort_order.asc(), Product.id.asc())
        .all()
    )
    code = normalize_lang(lang)
    return [present("products", ProductOut, row, code) for row in rows]


@public_router.get("/{slug}", response_model=ProductOut)
def get_product(slug: str, lang: str = "fa", db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.slug == slug, Product.is_active.is_(True)).first()
    if not product:
        raise HTTPException(status_code=404, detail="محصول پیدا نشد")
    return present("products", ProductOut, product, normalize_lang(lang))


@admin_router.get("", response_model=list[ProductOut])
def list_products(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.sort_order.asc(), Product.id.asc()).all()


@admin_router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductIn, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Product).filter(Product.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="این نامک قبلاً استفاده شده است")
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@admin_router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductIn,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="محصول پیدا نشد")
    exists = db.query(Product).filter(Product.slug == payload.slug, Product.id != product_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="این نامک قبلاً استفاده شده است")
    for key, value in payload.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@admin_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="محصول پیدا نشد")
    db.delete(product)
    db.commit()
