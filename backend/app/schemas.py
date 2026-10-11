from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)


class SlideIn(BaseModel):
    title: str
    subtitle: str = ""
    description: str = ""
    image_url: str = ""
    cta_primary_text: str = "بیشتر بدانید"
    cta_primary_link: str = "/about"
    cta_secondary_text: str = "مشاهده محصولات"
    cta_secondary_link: str = "/products"
    sort_order: int = 0
    is_active: bool = True


class SlideOut(SlideIn):
    id: int

    model_config = {"from_attributes": True}


class ProductIn(BaseModel):
    title: str
    slug: str
    summary: str = ""
    description: str = ""
    image_url: str = ""
    sort_order: int = 0
    is_active: bool = True


class ProductOut(ProductIn):
    id: int
    details: str = "{}"

    model_config = {"from_attributes": True}


class ServiceIn(BaseModel):
    title: str
    slug: str
    description: str = ""
    icon: str = "star"
    image_url: str = ""
    sort_order: int = 0


class ServiceOut(ServiceIn):
    id: int
    details: str = "{}"

    model_config = {"from_attributes": True}


class FeatureOut(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    sort_order: int

    model_config = {"from_attributes": True}


class ArticleIn(BaseModel):
    title: str
    slug: str
    excerpt: str = ""
    content: str = ""
    image_url: str = ""


class ArticleOut(ArticleIn):
    id: int
    published_at: datetime

    model_config = {"from_attributes": True}


class StatOut(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    sort_order: int

    model_config = {"from_attributes": True}


class SettingsOut(BaseModel):
    items: dict[str, str]
    features: list[FeatureOut]
    stats: list[StatOut]


class ContactIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(default="", max_length=40)
    subject: str = Field(default="", max_length=200)
    body: str = Field(min_length=5, max_length=5000)


class MessageOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    subject: str
    body: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
