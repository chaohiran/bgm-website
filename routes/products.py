from flask import Blueprint, render_template, request, abort, url_for
from collections import defaultdict
from database import get_db
from utils.admin_guard import admin_required

products_bp = Blueprint("products", __name__)


# =========================
# LIST PRODUCTS (หน้า /products)
# =========================
@products_bp.get("/")
def products_list():

    q = (request.args.get("q") or "").strip()
    cat_filter = request.args.get("cat")

    db = get_db()

    if q:
        items = db.execute("""
            SELECT * FROM products
            WHERE name_key LIKE ?
            ORDER BY id ASC
        """, (f"%{q}%",)).fetchall()
    else:
        items = db.execute("""
            SELECT * FROM products
            ORDER BY id ASC
        """).fetchall()

    db.close()

    # filter category
    if cat_filter:
        items = [p for p in items if p["category_key"] == cat_filter]

    grouped_items = defaultdict(list)

    for p in items:
        grouped_items[p["category_key"]].append(p)

    return render_template(
        "products.html",
        grouped_items=grouped_items,
        q=q,
        cat_filter=cat_filter
    )


# =========================
# CATEGORY PAGE
# =========================
@products_bp.get("/category/<category>")
def products_category(category):

    db = get_db()

    items = db.execute("""
        SELECT * FROM products
        WHERE category_key = ?
        ORDER BY id ASC
    """, (category,)).fetchall()

    db.close()

    if not items:
        abort(404)

    return render_template(
        "product_category.html",
        items=items,
        category=category,
    )


# =========================
# PRODUCT DETAIL
# =========================
@products_bp.get("/<category>/<slug>")
def product_detail(category, slug):

    db = get_db()

    product = db.execute("""
        SELECT * FROM products
        WHERE slug = ?
    """, (slug,)).fetchone()

    db.close()

    if not product:
        abort(404)

    if product["category_key"] != category:
        abort(404)

    return render_template(
        "product_detail.html",
        product=product,
    )