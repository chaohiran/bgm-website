from flask import Blueprint, request, session, redirect

lang_bp = Blueprint("lang", __name__)

@lang_bp.get("/set/<lang_code>")
def set_lang(lang_code):
    if lang_code in ["th", "en", "vi"]:
        session["lang"] = lang_code
    return redirect(request.referrer or "/")
