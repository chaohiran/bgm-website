from flask import request, session
from services.translations import TRANSLATIONS

SUPPORTED_LANGS = ["th", "en", "vi"]
DEFAULT_LANG = "th"

def get_lang():
    # 1) ?lang=en
    q = request.args.get("lang")
    if q in SUPPORTED_LANGS:
        session["lang"] = q
        return q

    # 2) session
    s = session.get("lang")
    if s in SUPPORTED_LANGS:
        return s

    # 3) header auto-detect (optional)
    # Accept-Language: en-US,en;q=0.9,th;q=0.8 ...
    al = (request.headers.get("Accept-Language") or "").lower()
    if al.startswith("vi"):
        return "vi"
    if al.startswith("en"):
        return "en"
    if al.startswith("th"):
        return "th"

    return DEFAULT_LANG

def t(key: str, **kwargs):
    lang = get_lang()
    text = TRANSLATIONS.get(lang, {}).get(key) \
           or TRANSLATIONS[DEFAULT_LANG].get(key) \
           or key

    # รองรับ {name} ในข้อความ ถ้าต้องการ
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
