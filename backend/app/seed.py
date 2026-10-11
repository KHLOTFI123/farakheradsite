from urllib.error import URLError
from urllib.request import urlopen

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.config import settings
from app.database import engine
from app.models import Article, Feature, Product, Service, SiteSetting, Slide, Stat, User
from app.product_content import details_json
from app.service_content import LIVE_SERVICES, NESTED_OFFERING_TITLES, TITLE_SLUGS
from app.service_content import details_json as service_details_json

LIVE = "https://farakheradgroup.ir/images"


def local_image(filename: str) -> str:
    dest = settings.upload_dir / filename
    if not dest.exists():
        try:
            with urlopen(f"{LIVE}/{filename}", timeout=5) as response:
                dest.write_bytes(response.read())
        except (OSError, URLError, TimeoutError, ValueError):
            return f"{LIVE}/{filename}"
    return f"/api/uploads/{filename}"


def replace_rows(db: Session, model, rows) -> None:
    db.query(model).delete()
    db.add_all(rows)


def _unique_slug(used: set[str], title: str, service_id: int | None) -> str:
    base = TITLE_SLUGS.get(title) or f"service-{service_id or 'item'}"
    slug = base
    index = 1
    while slug in used:
        index += 1
        slug = f"{base}-{index}"
    used.add(slug)
    return slug


def upsert_live_services(db: Session) -> None:
    for item in LIVE_SERVICES:
        row = db.query(Service).filter(Service.slug == item["slug"]).first()
        if not row:
            row = db.query(Service).filter(Service.title == item["title"]).first()
        payload = {
            **item,
            "details": service_details_json(item["slug"]),
        }
        if row:
            for key, value in payload.items():
                setattr(row, key, value)
        else:
            db.add(Service(**payload))
    db.flush()
    extras = db.query(Service).filter(Service.title.in_(NESTED_OFFERING_TITLES)).all()
    for row in extras:
        db.delete(row)
    db.flush()
    used = {row.slug for row in db.query(Service).all() if row.slug}
    for row in db.query(Service).order_by(Service.id.asc()).all():
        if not row.slug:
            row.slug = _unique_slug(used, row.title, row.id)
        if not row.details:
            row.details = "{}"


def ensure_settings(db: Session, rows: list[SiteSetting]) -> None:
    existing = {row.key: row for row in db.query(SiteSetting).all()}
    for row in rows:
        current = existing.get(row.key)
        if current is None:
            db.add(row)
            continue
        # Keep operator edits; only sync site_url from environment.
        if row.key == "site_url":
            current.value = row.value


def seed_database(db: Session) -> None:
    admin = db.query(User).filter(User.username == settings.admin_username).first()
    if not admin:
        db.add(
            User(
                username=settings.admin_username,
                hashed_password=hash_password(settings.admin_password),
            )
        )
    elif settings.reset_admin_password:
        admin.hashed_password = hash_password(settings.admin_password)

    if db.query(Slide).count() == 0:
        replace_rows(
            db,
            Slide,
        [
            Slide(
                title="راهکارهای هوش مصنوعی سازمانی",
                subtitle="هوش مصنوعی برای آینده کسب‌وکار شما",
                description=(
                    "فرا خرد توسعه‌دهنده نرم‌افزارهای سازمانی، راهکارهای هوش مصنوعی "
                    "و محصولات زیرساختی برای تحول دیجیتال کسب‌وکارهاست."
                ),
                image_url=local_image("hero-ai.jpg"),
                cta_primary_text="مشاهده محصولات",
                cta_primary_link="/products",
                cta_secondary_text="تماس با ما",
                cta_secondary_link="/contact",
                sort_order=1,
            ),
            Slide(
                title="شرکت فناوری اطلاعات فرا خرد",
                subtitle="پیشرو در نرم‌افزار سازمانی و هوش مصنوعی",
                description=(
                    "فرا خرد با تمرکز بر نیازهای سازمان‌های بزرگ، نرم‌افزارهای سازمانی، "
                    "راهکارهای هوش مصنوعی و محصولات زیرساختی توسعه می‌دهد."
                ),
                image_url=local_image("ai-infrastructure.jpg"),
                cta_primary_text="درباره ما",
                cta_primary_link="/about",
                cta_secondary_text="خدمات ما",
                cta_secondary_link="/services",
                sort_order=2,
            ),
        ],
    )

    if db.query(Product).count() == 0:
        replace_rows(
            db,
            Product,
            [
            Product(
                title="زیرساخت هوش مصنوعی سازمانی فراخرد",
                slug="enterprise-ai-platform",
                summary="زیرساخت خصوصی هوش مصنوعی شامل کلاستر GPU، سرو مدل، پایگاه داده برداری، API و استقرار سازمانی",
                description=(
                    "پلتفرم اختصاصی فراخرد برای اجرای هوش مصنوعی در مقیاس سازمانی؛ "
                    "هر آنچه سازمان برای ساخت، استقرار و مدیریت هوش مصنوعی نیاز دارد، در یک پلتفرم یکپارچه.\n\n"
                    "این پلتفرم تمام نیازهای سازمان را پوشش می‌دهد؛ از محیط کاری چندکاربره و مدیریت چرخه عمر مدل "
                    "تا مدیریت منابع GPU، ردیابی آزمایش‌ها و اتوماسیون خطوط لوله، همراه با امنیت، مقیاس‌پذیری، "
                    "پایش، کنترل دسترسی مبتنی بر نقش و امکان استقرار On-Premise یا ابری.\n\n"
                    "سازمان‌ها می‌توانند تمام پروژه‌های هوش مصنوعی خود را از یک پلتفرم واحد بسازند، مستقر کنند "
                    "و مدیریت نمایند؛ از مدیریت داده و آموزش مدل تا استقرار، سرویس‌دهی و پایش."
                ),
                image_url=local_image("ai-infrastructure.jpg"),
                details=details_json("enterprise-ai-platform"),
                sort_order=1,
            ),
            Product(
                title="دستیار هوش مصنوعی فراخرد",
                slug="ai-assistant",
                summary="دستیار سازمانی مبتنی بر مدل‌های زبانی بزرگ (LLM) برای سازمان‌ها",
                description=(
                    "بسیار فراتر از یک چت‌بات؛ یک دستیار هوش مصنوعی Agentic که وظایف کسب‌وکار را انجام می‌دهد "
                    "و مانند یک کارمند دیجیتال در کنار تیم شما کار می‌کند.\n\n"
                    "این دستیار مکالمات را درک می‌کند، زمینه گفتگو را به خاطر می‌سپارد، به سامانه‌های سازمانی متصل می‌شود، "
                    "فرایندها را خودکار می‌کند و اقدامات چندمرحله‌ای را اجرا می‌نماید.\n\n"
                    "با دسترسی به دانش سازمانی و یکپارچگی با APIها، دستیار فراخرد به‌عنوان یک کارمند دیجیتال "
                    "به واحدهای مختلف سازمان کمک می‌کند و بهره‌وری را افزایش می‌دهد."
                ),
                image_url=local_image("ai-assistant.jpg"),
                details=details_json("ai-assistant"),
                sort_order=2,
            ),
            Product(
                title="هوش تجاری تعاملی فراخرد",
                slug="intelligent-bi",
                summary="راهکار هوش تجاری مبتنی بر هوش مصنوعی برای تحلیل داده و تصمیم‌گیری سازمانی",
                description=(
                    "پلتفرم هوش تجاری مبتنی بر هوش مصنوعی؛ سوال خود را به فارسی یا انگلیسی بپرسید و "
                    "بدون نیاز به دانش SQL، پاسخ، جدول و نمودار دریافت کنید.\n\n"
                    "کاربران کسب‌وکار می‌توانند بدون نوشتن حتی یک خط SQL داده‌های سازمان را تحلیل کنند. "
                    "پلتفرم به‌صورت خودکار ساختار پایگاه داده را درک می‌کند، به چند پایگاه داده متصل می‌شود، "
                    "SQL را به‌صورت پویا تولید و ایمن اجرا می‌کند و نتایج را در قالب جدول، نمودار و توضیح "
                    "به زبان طبیعی ارائه می‌دهد."
                ),
                image_url=local_image("query-builder.jpg"),
                details=details_json("intelligent-bi"),
                sort_order=3,
            ),
            Product(
                title="API Gateway",
                slug="api-gateway",
                summary="درگاه API سازمانی با احراز هویت، مسیریابی، محدودیت نرخ، مانیتورینگ و امنیت",
                description=(
                    "یک درگاه API مدرن سازمانی با پیکربندی کاملاً گرافیکی و موتور صورتحساب داخلی؛ "
                    "تا حتی یک ریال از درآمد API شما از دست نرود.\n\n"
                    "برخلاف درگاه‌های سنتی، همه‌چیز از طریق یک رابط گرافیکی شهودی قابل پیکربندی است؛ "
                    "بدون نیاز به فایل‌های پیکربندی دستی، بدون ویرایش YAML و بدون پیکربندی خط فرمان. "
                    "تغییرات به‌صورت آنی اعمال می‌شوند.\n\n"
                    "موتور صورتحساب داخلی به‌صورت کامل در درگاه یکپارچه شده و مصرف API و هزینه مشتریان "
                    "را به‌صورت خودکار محاسبه می‌کند."
                ),
                image_url=local_image("api-gateway.jpg"),
                details=details_json("api-gateway"),
                sort_order=4,
            ),
            Product(
                title="سامانه آنلاین نوبت‌دهی و مدیریت صف",
                slug="online-queue-system",
                summary="پلتفرم نوبت‌دهی آنلاین و مدیریت صف برای بیمارستان‌ها، کلینیک‌ها، بانک‌ها و سازمان‌ها",
                description=(
                    "یک پلتفرم کامل رزرو آنلاین و مدیریت صف؛ کل فرایند نوبت‌دهی و مدیریت صف سازمان شما را دیجیتال می‌کند.\n\n"
                    "این سامانه به سازمان‌ها امکان می‌دهد برای هر نوع خدمتی نوبت‌دهی آنلاین ارائه دهند؛ "
                    "از رزرو آنلاین و مدیریت صف تا اطلاع‌رسانی پیامکی، داشبوردهای مدیریتی و پنل اپراتور باجه.\n\n"
                    "با پشتیبانی از چند شعبه، مدیریت خدمات و گزارش‌های تحلیلی، این پلتفرم برای بیمارستان‌ها، "
                    "کلینیک‌ها، بانک‌ها، سازمان‌های دولتی و سازمان‌های بزرگ مناسب است."
                ),
                image_url=local_image("queue-system-multi.jpg"),
                details=details_json("online-queue-system"),
                sort_order=5,
            ),
        ],
    )

    replace_rows(
        db,
        Feature,
        [
            Feature(title="خودکارسازی", description="اتوماسیون فرآیندهای تکراری و کاهش خطای انسانی با هوش مصنوعی", icon="settings", sort_order=1),
            Feature(title="افزایش بهره‌وری", description="تسریع انجام کارها و آزادسازی منابع انسانی برای وظایف استراتژیک", icon="chart", sort_order=2),
            Feature(title="تصمیم‌گیری هوشمند", description="تحلیل داده‌ها و ارائه بینش‌های عملی برای تصمیم‌گیری بهتر مدیران", icon="bulb", sort_order=3),
            Feature(title="کاهش هزینه", description="بهینه‌سازی منابع و کاهش هزینه‌های عملیاتی با راهکارهای هوشمند", icon="database", sort_order=4),
            Feature(title="تحلیل داده", description="استخراج الگوها و بینش‌های ارزشمند از حجم عظیم داده‌های سازمانی", icon="layers", sort_order=5),
        ],
    )

    upsert_live_services(db)

    replace_rows(
        db,
        Stat,
        [
            Stat(title="تیم متخصص", description="تجربه در نرم‌افزار سازمانی و هوش مصنوعی", icon="users", sort_order=1),
            Stat(title="فناوری‌های مدرن", description="جدیدترین تکنولوژی‌ها و بهترین شیوه‌ها", icon="code", sort_order=2),
            Stat(title="امنیت بالا", description="استانداردهای امنیتی سازمانی", icon="shield", sort_order=3),
            Stat(title="معماری مقیاس‌پذیر", description="زیرساختی که با رشد شما گسترش می‌یابد", icon="layers", sort_order=4),
        ],
    )

    if db.query(Article).count() == 0:
        replace_rows(
            db,
            Article,
            [
            Article(
                title="مزایای هوش مصنوعی برای کسب‌وکار",
                slug="ai-benefits-for-business",
                excerpt="هوش مصنوعی نحوه عملکرد سازمان‌ها را متحول می‌کند و فرصت‌های جدیدی برای رشد و نوآوری ایجاد می‌کند.",
                content=(
                    "هوش مصنوعی نحوه عملکرد سازمان‌ها را متحول می‌کند و فرصت‌های جدیدی برای رشد و نوآوری ایجاد می‌کند. "
                    "سازمان‌هایی که فرآیندهای تکراری را خودکار می‌کنند، خطای انسانی را کاهش می‌دهند، بهره‌وری را بالا می‌برند "
                    "و منابع انسانی را برای وظایف استراتژیک آزاد می‌کنند.\n\n"
                    "تحلیل داده و تصمیم‌گیری هوشمند به مدیران بینش عملی می‌دهد. به‌جای گزارش‌های ایستا، "
                    "مدل‌ها الگوهای پنهان را استخراج می‌کنند و پیشنهادهای قابل‌اجرا ارائه می‌دهند. "
                    "تجربه مشتری نیز با خدمات شخصی‌سازی‌شده، پاسخ سریع‌تر و پشتیبانی هوشمند بهبود می‌یابد.\n\n"
                    "کاهش هزینه عملیاتی نتیجه مستقیم بهینه‌سازی منابع و حذف کارهای دستی است. "
                    "با استقرار خصوصی مدل‌ها، حاکمیت داده حفظ می‌شود و سازمان می‌تواند بدون وابستگی به سرویس‌های عمومی، "
                    "هوش مصنوعی را در مقیاس سازمانی اجرا کند.\n\n"
                    "فرا خرد این مسیر را با پلتفرم هوش مصنوعی سازمانی، دستیار Agentic، هوش تجاری تعاملی "
                    "و خدمات DevOps و MLOps همراهی می‌کند تا تحول دیجیتال از ایده به محصول پایدار برسد."
                ),
                image_url=local_image("hero-ai.jpg"),
            ),
            Article(
                title="خدمات DevOps فرا خرد",
                slug="devops-services",
                excerpt="طراحی چرخه کامل توسعه نرم‌افزار؛ از مدیریت کد تا تست، انتشار و مانیتورینگ.",
                content=(
                    "هیچ دو سازمانی نیاز یکسانی ندارند. فرا خرد زیرساخت DevOps را متناسب با اندازه تیم، "
                    "معماری محصولات و اهداف کسب‌وکار طراحی می‌کند.\n\n"
                    "خدمات شامل طراحی معماری DevOps، پایپ‌لاین CI/CD، راه‌اندازی GitLab، Kubernetes و Docker، "
                    "اتوماسیون زیرساخت، مانیتورینگ و بهینه‌سازی فرآیند انتشار است. "
                    "هدف این است که هر تغییر کد با آزمون خودکار، استقرار تکرارپذیر و پایش زنده به محیط تولید برسد.\n\n"
                    "با استانداردسازی محیط‌ها، زمان انتشار کاهش می‌یابد و خطای دستی کمتر می‌شود. "
                    "تیم‌ها می‌توانند روی محصول تمرکز کنند و زیرساخت به‌صورت کد مدیریت شود. "
                    "این رویکرد برای سازمان‌هایی که چند محصول یا چند محیط دارند، ثبات و مقیاس‌پذیری ایجاد می‌کند.\n\n"
                    "فرا خرد از طراحی تا استقرار کنار تیم فنی شما می‌ماند تا چرخه توسعه، تست و انتشار "
                    "به یک فرآیند قابل‌اعتماد و قابل‌اندازه‌گیری تبدیل شود."
                ),
                image_url=local_image("api-gateway.jpg"),
            ),
            Article(
                title="خدمات MLOps فرا خرد",
                slug="mlops-services",
                excerpt="شروع مسیر هوش مصنوعی با زیرساخت مناسب و استانداردهای صنعتی.",
                content=(
                    "فرا خرد به سازمان‌ها کمک می‌کند پروژه‌های هوش مصنوعی را از ایده تا Production پیش ببرند. "
                    "زیرساخت AI متناسب با نوع مدل، حجم داده، نیاز پردازشی و اهداف کسب‌وکار طراحی می‌شود.\n\n"
                    "خدمات شامل مدیریت مدل‌های زبانی بزرگ، زیرساخت GPU، نسخه‌بندی داده و مدل، "
                    "خطوط لوله آموزش و استقرار، و پایش عملکرد در محیط تولید است. "
                    "بدون این لایه‌ها، مدل‌ها در آزمایشگاه می‌مانند و به ارزش عملیاتی تبدیل نمی‌شوند.\n\n"
                    "MLOps فاصله بین تیم داده و تیم عملیات را کم می‌کند: آموزش تکرارپذیر، استقرار کنترل‌شده، "
                    "بازگشت سریع در صورت افت کیفیت، و حاکمیت دسترسی روی داده و مدل. "
                    "سازمان می‌تواند چند مدل را همزمان مدیریت کند و هزینه GPU را بهینه نگه دارد.\n\n"
                    "با همراهی فرا خرد، مسیر هوش مصنوعی از اثبات مفهوم به سرویس پایدار سازمانی تبدیل می‌شود "
                    "و استانداردهای امنیتی و عملیاتی از ابتدا در معماری لحاظ می‌گردد."
                ),
                image_url=local_image("ai-infrastructure.jpg"),
            ),
            ],
        )

    ensure_settings(
        db,
        [
            SiteSetting(key="company_name", value="فرا خرد"),
            SiteSetting(key="tagline", value="راهکارهای هوش مصنوعی سازمانی"),
            SiteSetting(key="about_title", value="درباره فرا خرد"),
            SiteSetting(
                key="about_text",
                value=(
                    "شرکت فناوری اطلاعات فرا خرد، پیشرو در توسعه نرم‌افزارهای سازمانی و راهکارهای هوش مصنوعی. "
                    "فرا خرد یک شرکت فناوری اطلاعات است که با تمرکز بر نیازهای سازمان‌های بزرگ، نرم‌افزارهای سازمانی، "
                    "راهکارهای هوش مصنوعی و محصولات زیرساختی توسعه می‌دهد. "
                    "ما با بهره‌گیری از جدیدترین فناوری‌ها و تیمی متخصص، به کسب‌وکارها کمک می‌کنیم تا با هوش مصنوعی "
                    "و تحول دیجیتال، عملکرد خود را به سطح جدیدی ارتقا دهند."
                ),
            ),
            SiteSetting(key="cta_kicker", value="چرا فرا خرد؟"),
            SiteSetting(key="cta_title", value="آماده تحول دیجیتال کسب‌وکار خود هستید؟"),
            SiteSetting(
                key="cta_text",
                value="با تیم متخصص فرا خرد تماس بگیرید و از مشاوره رایگان برای راهکارهای هوش مصنوعی و نرم‌افزار سازمانی بهره‌مند شوید.",
            ),
            SiteSetting(key="footer_text", value="توسعه‌دهنده نرم‌افزارهای سازمانی، راهکارهای هوش مصنوعی و محصولات زیرساختی"),
            SiteSetting(key="email", value="info@farakherad.com"),
            SiteSetting(key="phone", value="02177132703"),
            SiteSetting(key="mobile", value="09121788139"),
            SiteSetting(key="site_url", value=settings.site_url),
            SiteSetting(key="address", value="تهران، ایران"),
            SiteSetting(
                key="linkedin",
                value="https://www.linkedin.com/company/شرکت-فناوری-هوشمند-نوین-فراخرد/posts/?feedView=all",
            ),
        ],
    )

    db.commit()
    try:
        with engine.begin() as connection:
            connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_services_slug ON services (slug)"))
    except SQLAlchemyError:
        pass
