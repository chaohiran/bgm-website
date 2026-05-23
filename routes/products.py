<<<<<<< HEAD
from flask import Blueprint, render_template, abort
from database import get_db

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)


# =========================
# 📦 LIST CATEGORIES
=======
from flask import Blueprint, render_template, request, abort, url_for
from collections import defaultdict
from database import get_db
from utils.admin_guard import admin_required

products_bp = Blueprint("products", __name__)


# =========================
# LIST PRODUCTS (หน้า /products)
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf
# =========================
@products_bp.get("/")
def products_list():

<<<<<<< HEAD
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
=======
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
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf
    )


# =========================
<<<<<<< HEAD
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
=======
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
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf
    )


# =========================
<<<<<<< HEAD
# 📄 PRODUCT DETAIL
# =========================
@products_bp.get("/<slug>")
def product_detail(slug):
=======
# PRODUCT DETAIL
# =========================
@products_bp.get("/<category>/<slug>")
def product_detail(category, slug):
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf

    db = get_db()

    product = db.execute("""
<<<<<<< HEAD
        SELECT
            p.*,
            c.key AS category_key,
            c.name_th AS category_name_th,
            c.name_en AS category_name_en
        FROM products p
        JOIN categories c
            ON p.category_id = c.id
        WHERE p.slug = ?
=======
        SELECT * FROM products
        WHERE slug = ?
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf
    """, (slug,)).fetchone()

    db.close()

    if not product:
        abort(404)

<<<<<<< HEAD
    return render_template(
        "product_detail.html",
        product=product
=======
    if product["category_key"] != category:
        abort(404)

    return render_template(
        "product_detail.html",
        product=product,
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf
    )