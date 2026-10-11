from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.i18n import localize_settings, normalize_lang
from app.models import Feature, SiteSetting, Stat
from app.schemas import SettingsOut, StatOut, FeatureOut

router = APIRouter(prefix="/api", tags=["content"])


@router.get("/settings", response_model=SettingsOut)
def get_settings(lang: str = "fa", db: Session = Depends(get_db)):
    items = {row.key: row.value for row in db.query(SiteSetting).all()}
    features = db.query(Feature).order_by(Feature.sort_order.asc()).all()
    stats = db.query(Stat).order_by(Stat.sort_order.asc()).all()
    payload = SettingsOut(
        items=items,
        features=[FeatureOut.model_validate(item) for item in features],
        stats=[StatOut.model_validate(item) for item in stats],
    ).model_dump(mode="json")
    return localize_settings(payload, normalize_lang(lang))
