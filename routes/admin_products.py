from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort
)

from utils.admin_guard import admin_required
from database import get_db

from werkzeug.utils import secure_filename

import os
import uuid


admin_products_bp = Blueprint(
    "admin_products",
    __name__,
    url_prefix="/products"
)

UPLOAD_FOLDER = "static/uploads/products"


# =========================
# 📦 LIST PRODUCTS
# =========================
@admin_products_bp.route("/")
@admin_required
def index():

    db = get_db()

    products = db.execute("""
        SELECT * FROM products
        ORDER BY id DESC
    """).fetchall()

    db.close()

    return render_template(
        "products.html",
        products=products
    )


# =========================
# ➕ CREATE PRODUCT
# =========================
@admin_products_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():

    error = None

    if request.method == "POST":

        slug = (request.form.get("slug") or "").strip()
        name_key = (request.form.get("name_key") or "").strip()
        category_key = (request.form.get("category_key") or "").strip()
        short_key = (request.form.get("short_key") or "").strip()

        # =========================
        # VALIDATION
        # =========================
        if not slug or not name_key or not category_key:

            error = "กรุณากรอกข้อมูลให้ครบ"

            return render_template(
                "admin/products/create.html",
                error=error
            )

        # =========================
        # IMAGE UPLOAD
        # =========================
        file = request.files.get("image")

        filename = "default.jpg"

        if file and file.filename:

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            ext = file.filename.rsplit(".", 1)[-1].lower()

            filename = f"{uuid.uuid4().hex}.{ext}"

            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            file.save(filepath)

        # =========================
        # SAVE DB
        # =========================
        try:

            db = get_db()

            db.execute("""
                INSERT INTO products
                (slug, name_key, category_key, short_key, image)
                VALUES (?, ?, ?, ?, ?)
            """, (
                slug,
                name_key,
                category_key,
                short_key,
                filename
            ))

            db.commit()
            db.close()

            return redirect(
                url_for("admin_products.index")
            )

        except Exception as e:

            error = f"เกิดข้อผิดพลาด: {str(e)}"

            return render_template(
                "admin/products/create.html",
                error=error
            )

    return render_template(
        "admin/products/create.html"
    )


# =========================
# ✏️ EDIT PRODUCT
# =========================
@admin_products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(product_id):

    db = get_db()

    product = db.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if not product:
        db.close()
        abort(404)

    if request.method == "POST":

        slug = request.form["slug"]
        name_key = request.form["name_key"]
        category_key = request.form["category_key"]
        short_key = request.form["short_key"]

        image = product["image"]

        # =========================
        # FILE UPLOAD
        # =========================
        file = request.files.get("image_file")

        if file and file.filename:

            filename = secure_filename(file.filename)

            upload_path = os.path.join(
                "static",
                "img",
                "products",
                filename
            )

            file.save(upload_path)

            image = filename

        db.execute("""
            UPDATE products
            SET slug=?, name_key=?, category_key=?, short_key=?, image=?
            WHERE id=?
        """, (
            slug,
            name_key,
            category_key,
            short_key,
            image,
            product_id
        ))

        db.commit()
        db.close()

        return redirect(url_for("admin_products.index"))

    db.close()

    return render_template(
        "admin/products/edit.html",
        product=product
    )

# =========================
# 🗑 DELETE PRODUCT
# =========================
@admin_products_bp.route("/delete/<int:product_id>")
@admin_required
def delete(product_id):

    db = get_db()

    product = db.execute("""
        SELECT * FROM products
        WHERE id = ?
    """, (product_id,)).fetchone()

    if product:

        # delete image
        if (
            product["image"]
            and product["image"] != "default.jpg"
        ):

            image_path = os.path.join(
                UPLOAD_FOLDER,
                product["image"]
            )

            if os.path.exists(image_path):
                os.remove(image_path)

        db.execute("""
            DELETE FROM products
            WHERE id = ?
        """, (product_id,))

        db.commit()

    db.close()

    return redirect(
        url_for("admin_products.index")
    )