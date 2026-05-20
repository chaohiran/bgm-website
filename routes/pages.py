from flask import Blueprint, render_template, abort
from database import get_db, get_company_profile

pages_bp = Blueprint("pages", __name__)


# =========================
# STATIC PAGE FROM DB (หรือ fallback)
# =========================
@pages_bp.get("/<slug>")
def page(slug):

    # ตัวอย่าง: pages ยังเป็น dict เดิม (ยังไม่ย้าย DB)
    # ถ้าคุณยังไม่ได้ทำ table pages → ใช้ของเดิมไปก่อน

    pages = {
        "about": {
            "title_key": "about_title",
            "lead_key": "about_lead",
        },
        "services": {
            "title_key": "services_title",
            "lead_key": "services_lead",
        },
        "contact": {
            "title_key": "contact_title",
            "lead_key": "contact_lead",
        },
    }

    p = pages.get(slug)

    if not p:
        abort(404)

    return render_template(
        "page.html",
        page=p,
        slug=slug,
        profile=get_company_profile()
    )