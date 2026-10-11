import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth import get_current_user
from app.config import settings
from app.models import User
from app.security import sniff_image_suffix

router = APIRouter(prefix="/api/admin/upload", tags=["admin-upload"])

ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@router.post("")
async def upload_image(_: User = Depends(get_current_user), file: UploadFile = File(...)):
    declared = Path(file.filename or "").suffix.lower()
    if declared == ".jpeg":
        declared = ".jpg"
    if declared and declared not in ALLOWED:
        raise HTTPException(status_code=400, detail="فقط تصویر با فرمت jpg، png، webp یا gif مجاز است")

    content = await file.read(settings.max_upload_bytes + 1)
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(status_code=400, detail="حجم فایل بیش از حد مجاز است")
    if not content:
        raise HTTPException(status_code=400, detail="فایل خالی است")

    sniffed = sniff_image_suffix(content)
    if not sniffed:
        raise HTTPException(status_code=400, detail="محتوای فایل تصویر معتبر نیست")
    if declared and declared != sniffed:
        raise HTTPException(status_code=400, detail="پسوند فایل با محتوای تصویر هم‌خوانی ندارد")

    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    name = f"{uuid.uuid4().hex}{sniffed}"
    dest = (settings.upload_dir / name).resolve()
    if dest.parent != settings.upload_dir.resolve():
        raise HTTPException(status_code=400, detail="مسیر ذخیره نامعتبر است")
    dest.write_bytes(content)
    return {"url": f"/api/uploads/{name}"}
