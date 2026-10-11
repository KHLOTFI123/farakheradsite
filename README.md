# سایت فراخرد

سایت شرکتی فراخرد با یک فرایند: React، FastAPI و SQLite. زبان‌ها: فارسی، انگلیسی، عربی، دری، ترکی و روسی.

## اجرای کامل با Docker

در ریشه پروژه:

```bash
docker compose up --build
```

- سایت: http://localhost:3000
- API: http://localhost:3000/api/health
- پنل ادمین: http://localhost:3000/admin

ورود پیش‌فرض ادمین: `admin` / `admin123` (فقط برای توسعه؛ در `.env` عوض کنید)

### نکات امنیتی برای اینترنت

- `ENVIRONMENT=production`
- `SECRET_KEY` تصادفی و حداقل ۳۲ کاراکتر
- `ADMIN_PASSWORD` قوی؛ رمز ادمین دیگر با هر ری‌استارت عوض نمی‌شود مگر `RESET_ADMIN_PASSWORD=true`
- `CORS_ORIGINS` را به دامنه واقعی محدود کنید
- پشت پروکسی فقط پورت ۸۰/۴۴۳ را باز کنید؛ سرویس را روی `127.0.0.1` بایند کنید
- `/docs` و OpenAPI در حالت production خاموش است

## اجرای محلی روی کامپیوتر

۱. بک‌اند (SQLite، بدون سرویس جدا):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy ..\.env .env
uvicorn app.main:app --reload --port 8000
```

۲. فرانت:

```bash
cd frontend
npm install
npm run dev
```

سایت توسعه روی http://localhost:5173 باز می‌شود و درخواست‌های `/api` به بک‌اند پروکسی می‌شوند.

## امکانات پنل ادمین

- تغییر تصاویر و متن اسلایدشو
- افزودن و ویرایش معرفی محصولات
- مشاهده، خواندن و حذف پیام‌های فرم تماس
