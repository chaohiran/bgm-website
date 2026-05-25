from flask import Blueprint, render_template, abort
from database import get_db

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)

# =========================
# 📂 CATEGORY LIST PAGE
# =========================
@products_bp.get("/")
def products_list():

    db = get_db()

    categories = db.execute("""
        SELECT *
        FROM categories
        ORDER BY sort_order ASC, id ASC
    """).fetchall()

    db.close()

    return render_template(
        "products.html",
        categories=categories
    )


# =========================
# 📦 PRODUCTS BY CATEGORY
# =========================
@products_bp.get("/category/<key>")
def products_category(key):

    db = get_db()

    # CATEGORY
    category = db.execute("""
        SELECT *
        FROM categories
        WHERE key = ?
    """, (key,)).fetchone()

    if not category:
        db.close()
        abort(404)

    # PRODUCTS
    items = db.execute("""
        SELECT
            p.*,
            c.key AS category_key
        FROM products p
        JOIN categories c
            ON p.category_id = c.id
        WHERE c.key = ?
        ORDER BY p.sort_order ASC, p.id DESC
    """, (key,)).fetchall()

    db.close()

    return render_template(
        "product_category.html",
        category=category,
        items=items
    )


# =========================
# 📄 PRODUCT DETAIL
# =========================
@products_bp.get("/<category_key>/<slug>")
def product_detail(category_key, slug):

    db = get_db()

    product = db.execute("""
        SELECT
            p.*,
            c.key AS category_key,
            c.name_th AS category_name_th,
            c.name_en AS category_name_en
        FROM products p
        JOIN categories c
            ON p.category_id = c.id
        WHERE p.slug = ?
    """, (slug,)).fetchone()

    db.close()

    # ❌ PRODUCT NOT FOUND
    if not product:
        abort(404)

    # ❌ CATEGORY URL NOT MATCH
    if product["category_key"] != category_key:
        abort(404)

    return render_template(
        "product_detail.html",
        product=product
    )