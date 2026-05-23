from flask import Blueprint, render_template
from flask import Blueprint, render_template
from database import get_db

home_bp = Blueprint("home", __name__)

@home_bp.get("/")
def index():

    profile = {
        "name": "BGM EXPLOSION PROOF",
        "tagline_key": "company_tagline",
        "phone": "+66 96-874-5916 / +66 83-815-5565",
        "email": "belgiumindustrial@gmail.com",
        "address_key": "company_address",
    }

    highlights = [
        {
            "title_key": "hl_full_service_title",
            "desc_key": "hl_full_service_desc",
        },
        {
            "title_key": "hl_pro_team_title",
            "desc_key": "hl_pro_team_desc",
        },
        {
            "title_key": "hl_standard_title",
            "desc_key": "hl_standard_desc",
        },
    ]

    return render_template(
        "index.html",
        profile=profile,
        highlights=highlights
    )
