import json
from copy import deepcopy

LOCALES = ("fa", "en", "ar", "fa-AF", "tr", "ru")
RTL = {"fa", "ar", "fa-AF"}
SKIP_KEYS = {
    "slug",
    "icon",
    "image_url",
    "email",
    "phone",
    "mobile",
    "linkedin",
    "site_url",
    "id",
    "sort_order",
    "is_active",
    "published_at",
    "related",
    "featured",
    "url",
    "canonical",
    "image",
    "site_url",
}


def normalize_lang(value: str | None) -> str:
    if value in LOCALES:
        return value
    return "fa"


def split_lang(path: str) -> tuple[str, str]:
    clean = path.split("?", 1)[0] or "/"
    parts = [part for part in clean.split("/") if part]
    if parts and parts[0] in LOCALES:
        rest = "/" + "/".join(parts[1:]) if len(parts) > 1 else "/"
        return parts[0], rest
    return "fa", clean if clean.startswith("/") else f"/{clean}"


def _pack(lang: str) -> dict:
    if lang == "fa":
        return {}
    from app import i18n_packs

    return i18n_packs.PACKS.get(lang, {})


def localize_mapping(kind: str, data: dict, lang: str) -> dict:
    lang = normalize_lang(lang)
    pack = _pack(lang)
    if not pack:
        return data
    out = dict(data)
    bucket = pack.get(kind, {})
    key = str(data.get("slug") or data.get("sort_order") or "")
    overlay = bucket.get(key) or bucket.get(data.get("title", ""))
    if isinstance(overlay, dict):
        for field in ("title", "subtitle", "description", "excerpt", "content", "summary"):
            if overlay.get(field):
                out[field] = overlay[field]
        for field in ("cta_primary_text", "cta_secondary_text"):
            if overlay.get(field):
                out[field] = overlay[field]
        if overlay.get("details") and "details" in out:
            try:
                base = json.loads(out.get("details") or "{}")
            except json.JSONDecodeError:
                base = {}
            details = dict(overlay["details"])
            if "related" not in details and isinstance(base, dict) and base.get("related"):
                details["related"] = base["related"]
            if "featured" not in details and isinstance(base, dict) and "featured" in base:
                details["featured"] = base["featured"]
            out["details"] = json.dumps(details, ensure_ascii=False)
    return out


def localize_settings(payload: dict, lang: str) -> dict:
    lang = normalize_lang(lang)
    pack = _pack(lang)
    if not pack:
        return payload
    out = deepcopy(payload)
    items = dict(out.get("items") or {})
    for key, value in (pack.get("settings") or {}).items():
        if value:
            items[key] = value
    out["items"] = items
    features = []
    feature_pack = pack.get("features") or {}
    for row in out.get("features") or []:
        features.append(localize_mapping("features", row, lang) if feature_pack else row)
    stats = []
    for row in out.get("stats") or []:
        stats.append(localize_mapping("stats", row, lang))
    out["features"] = features
    out["stats"] = stats
    return out


def localize_text(value: str, lang: str) -> str:
    pack = _pack(normalize_lang(lang))
    return (pack.get("ui") or {}).get(value, value)


def present(kind: str, schema, row, lang: str) -> dict:
    data = schema.model_validate(row).model_dump(mode="json")
    return localize_mapping(kind, data, lang)
