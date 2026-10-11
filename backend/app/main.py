import time
from contextlib import asynccontextmanager
from urllib.parse import quote, urlparse

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import OperationalError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine, ensure_schema
from app.routers import articles, auth, contact, content, products, seo, services, slides, upload
from app.security import SecurityHeadersMiddleware
from app.seed import seed_database


def wait_for_database() -> None:
    for attempt in range(30):
        try:
            with engine.connect() as connection:
                connection.exec_driver_sql("SELECT 1")
            return
        except OperationalError:
            time.sleep(1)
            if attempt == 29:
                raise


@asynccontextmanager
async def lifespan(_: FastAPI):
    wait_for_database()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    ensure_schema()
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


_docs = None if settings.is_production else "/docs"
_redoc = None if settings.is_production else "/redoc"
_openapi = None if settings.is_production else "/openapi.json"

app = FastAPI(
    title="Farakherad API",
    lifespan=lifespan,
    docs_url=_docs,
    redoc_url=_redoc,
    openapi_url=_openapi,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

if settings.is_production:
    _hosts = {"localhost", "127.0.0.1"}
    _site_host = urlparse(settings.site_url).hostname
    if _site_host:
        _hosts.add(_site_host)
        if not _site_host.startswith("www."):
            _hosts.add(f"www.{_site_host}")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=sorted(_hosts))

app.include_router(auth.router)
app.include_router(slides.public_router)
app.include_router(slides.admin_router)
app.include_router(products.public_router)
app.include_router(products.admin_router)
app.include_router(services.public_router)
app.include_router(services.admin_router)
app.include_router(articles.public_router)
app.include_router(articles.admin_router)
app.include_router(content.router)
app.include_router(contact.public_router)
app.include_router(contact.admin_router)
app.include_router(upload.router)
app.include_router(seo.router)

app.mount("/api/uploads", StaticFiles(directory=str(settings.upload_dir)), name="uploads")


@app.get("/api/health")
def health():
    return {"status": "ok"}


_BOTS = (
    "googlebot",
    "bingbot",
    "yandex",
    "baiduspider",
    "duckduckbot",
    "slurp",
    "facebookexternalhit",
    "twitterbot",
    "linkedinbot",
    "slackbot",
    "telegrambot",
    "whatsapp",
    "applebot",
    "semrushbot",
    "ahrefsbot",
    "dotbot",
    "mj12bot",
)


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            response = await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as exc:
            if exc.status_code != 404:
                raise
            return await super().get_response("index.html", scope)
        if response.status_code == 404:
            return await super().get_response("index.html", scope)
        return response


def _should_prerender(path: str) -> bool:
    if path.startswith("/api") or path.startswith("/assets") or path.startswith("/fonts") or path.startswith("/images"):
        return False
    return "." not in path.rsplit("/", 1)[-1]


@app.middleware("http")
async def prerender_bots(request: Request, call_next):
    agent = request.headers.get("user-agent", "").lower()
    path = request.url.path
    if request.method == "GET" and any(bot in agent for bot in _BOTS) and _should_prerender(path):
        headers = [(key, value) for key, value in request.scope["headers"] if key != b"x-original-uri"]
        headers.append((b"x-original-uri", quote(path, safe="/").encode()))
        request.scope["headers"] = headers
        request.scope["path"] = "/prerender"
        request.scope["raw_path"] = b"/prerender"
        request.scope["query_string"] = b""
    return await call_next(request)


if settings.static_dir.exists():
    app.mount("/", SPAStaticFiles(directory=str(settings.static_dir), html=True), name="site")
