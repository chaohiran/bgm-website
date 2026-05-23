from flask import Blueprint, render_template, abort
from database import get_db

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)


# =========================
# 📦 LIST CATEGORIES
# =========================
@products_bp.get("/")
def products_list():

    db = get_db()

    categories = db.execute("""
        SELECT *
        FROM categories
        ORDER BY id ASC
    """).fetchall()

    db.close()

    return render_template(
        "products.html",
        categories=categories
    )


# =========================
# 📂 CATEGORY PAGE
# =========================
@products_bp.get("/category/<slug>")
def products_category(slug):

    db = get_db()

    # ✅ ใช้ key แทน slug
    category = db.execute("""
        SELECT *
        FROM categories
        WHERE key = ?
    """, (slug,)).fetchone()

    if not category:
        db.close()
        abort(404)

    # ✅ ดึงสินค้าของหมวดนี้
    items = db.execute("""
        SELECT *
        FROM products
        WHERE category_id = ?
        ORDER BY id DESC
    """, (category["id"],)).fetchall()

    db.close()

    return render_template(
        "product_category.html",
        category=category,
        items=items
    )


# =========================
# 📄 PRODUCT DETAIL
# =========================
@products_bp.get("/<slug>")
def product_detail(slug):

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

    if not product:
        abort(404)

    return render_template(
        "product_detail.html",
        product=product
    )