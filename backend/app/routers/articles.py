from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.i18n import normalize_lang, present
from app.models import Article, User
from app.schemas import ArticleIn, ArticleOut

public_router = APIRouter(prefix="/api/articles", tags=["articles"])
admin_router = APIRouter(prefix="/api/admin/articles", tags=["admin-articles"])


@public_router.get("", response_model=list[ArticleOut])
def list_public_articles(lang: str = "fa", db: Session = Depends(get_db)):
    rows = db.query(Article).order_by(Article.published_at.desc()).all()
    code = normalize_lang(lang)
    return [present("articles", ArticleOut, row, code) for row in rows]


@public_router.get("/{slug}", response_model=ArticleOut)
def get_article(slug: str, lang: str = "fa", db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="مقاله پیدا نشد")
    return present("articles", ArticleOut, article, normalize_lang(lang))


@admin_router.get("", response_model=list[ArticleOut])
def list_articles(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Article).order_by(Article.published_at.desc()).all()


@admin_router.post("", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(payload: ArticleIn, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Article).filter(Article.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="این نامک قبلاً استفاده شده است")
    article = Article(**payload.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@admin_router.put("/{article_id}", response_model=ArticleOut)
def update_article(
    article_id: int,
    payload: ArticleIn,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="مقاله پیدا نشد")
    exists = db.query(Article).filter(Article.slug == payload.slug, Article.id != article_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="این نامک قبلاً استفاده شده است")
    for key, value in payload.model_dump().items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article


@admin_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="مقاله پیدا نشد")
    db.delete(article)
    db.commit()
