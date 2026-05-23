from flask import Blueprint, render_template, request, redirect, url_for, abort
from database import get_db
from utils.admin_guard import admin_required

import os
import uuid

admin_products_bp = Blueprint(
    "admin_products",
    __name__,
    url_prefix="/admin/products"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_FOLDER = os.path.normpath(
    os.path.join(BASE_DIR, "..", "static", "img", "products")
)

PDF_FOLDER = os.path.normpath(
    os.path.join(BASE_DIR, "..", "static", "pdf", "products")
)

# =========================
# SAVE PDF
# =========================
def save_pdf(file):
    if file and file.filename:
        os.makedirs(PDF_FOLDER, exist_ok=True)

        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext != "pdf":
            return None

        filename = f"{uuid.uuid4().hex}.pdf"
        path = os.path.join(PDF_FOLDER, filename)
        file.save(path)
        return filename

    return None


# =========================
# LIST
# =========================
@admin_products_bp.route("/")
@admin_required
def index():
    db = get_db()
    try:
        category = db.execute("""
            SELECT key FROM categories
            ORDER BY id ASC LIMIT 1
        """).fetchone()

        if category:
            return redirect(url_for(
                "products.products_category",
                slug=category["key"]
            ))

        return redirect(url_for("products.products_list"))

    finally:
        db.close()


# =========================
# CREATE
# =========================
@admin_products_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():

    db = get_db()

    try:
        categories = db.execute("""
            SELECT * FROM categories ORDER BY id ASC
        """).fetchall()

        if request.method == "POST":

            slug = request.form.get("slug")

            name_th = request.form.get("name_th")
            name_en = request.form.get("name_en")

            short_th = request.form.get("short_th")
            short_en = request.form.get("short_en")

            category_id = request.form.get("category_id")

            # validation
            if not name_th or not name_en:
                return "Name required", 400

            existing = db.execute("""
                SELECT id FROM products WHERE slug = ?
            """, (slug,)).fetchone()

            if existing:
                return "Slug already exists", 400

            # IMAGE
            image = None
            file = request.files.get("image_file")

            if file and file.filename:
                os.makedirs(IMAGE_FOLDER, exist_ok=True)

                ext = file.filename.rsplit(".", 1)[-1].lower()
                filename = f"{uuid.uuid4().hex}.{ext}"

                file.save(os.path.join(IMAGE_FOLDER, filename))
                image = filename

            # PDF
            catalog_pdf = save_pdf(request.files.get("catalog_pdf"))
            manual_pdf = save_pdf(request.files.get("manual_pdf"))
            other_pdf = save_pdf(request.files.get("other_pdf"))

            db.execute("""
                INSERT INTO products (
                    slug,
                    name_th,
                    name_en,
                    short_th,
                    short_en,
                    category_id,
                    image,
                    catalog_pdf,
                    manual_pdf,
                    other_pdf
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                slug,
                name_th,
                name_en,
                short_th,
                short_en,
                category_id,
                image,
                catalog_pdf,
                manual_pdf,
                other_pdf
            ))

            db.commit()

            return redirect(url_for("products.products_list"))

        return render_template(
            "admin/products/create.html",
            categories=categories
        )

    finally:
        db.close()


# =========================
# EDIT
# =========================
@admin_products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(product_id):

    db = get_db()

    try:
        product = db.execute("""
            SELECT * FROM products WHERE id = ?
        """, (product_id,)).fetchone()

        if not product:
            abort(404)

        categories = db.execute("""
            SELECT * FROM categories ORDER BY id ASC
        """).fetchall()

        if request.method == "POST":

            slug = request.form.get("slug")

            name_th = request.form.get("name_th")
            name_en = request.form.get("name_en")

            short_th = request.form.get("short_th")
            short_en = request.form.get("short_en")

            category_id = request.form.get("category_id")

            if not name_th or not name_en:
                return "Name required", 400

            existing = db.execute("""
                SELECT id FROM products
                WHERE slug = ? AND id != ?
            """, (slug, product_id)).fetchone()

            if existing:
                return "Slug already exists", 400

            # IMAGE
            image = product["image"]
            file = request.files.get("image_file")

            if file and file.filename:

                if image and image != "default.jpg":
                    old = os.path.join(IMAGE_FOLDER, image)
                    if os.path.exists(old):
                        os.remove(old)

                ext = file.filename.rsplit(".", 1)[-1].lower()
                filename = f"{uuid.uuid4().hex}.{ext}"

                file.save(os.path.join(IMAGE_FOLDER, filename))
                image = filename

            # PDF UPDATE
            def handle_pdf(old, new_file):
                new = save_pdf(new_file)

                if new and old:
                    path = os.path.join(PDF_FOLDER, old)
                    if os.path.exists(path):
                        os.remove(path)

                return new if new else old

            catalog_pdf = handle_pdf(product["catalog_pdf"], request.files.get("catalog_pdf"))
            manual_pdf = handle_pdf(product["manual_pdf"], request.files.get("manual_pdf"))
            other_pdf = handle_pdf(product["other_pdf"], request.files.get("other_pdf"))

            db.execute("""
                UPDATE products
                SET slug=?,
                    name_th=?,
                    name_en=?,
                    short_th=?,
                    short_en=?,
                    category_id=?,
                    image=?,
                    catalog_pdf=?,
                    manual_pdf=?,
                    other_pdf=?
                WHERE id=?
            """, (
                slug,
                name_th,
                name_en,
                short_th,
                short_en,
                category_id,
                image,
                catalog_pdf,
                manual_pdf,
                other_pdf,
                product_id
            ))

            db.commit()

            return redirect(url_for("products.products_list"))

        return render_template(
            "admin/products/edit.html",
            product=product,
            categories=categories
        )

    finally:
        db.close()


# =========================
# DELETE PRODUCT
# =========================
@admin_products_bp.route("/delete/<int:product_id>")
@admin_required
def delete(product_id):

    db = get_db()

    try:
        product = db.execute("""
            SELECT * FROM products WHERE id = ?
        """, (product_id,)).fetchone()

        if not product:
            abort(404)

        # delete image
        if product["image"] and product["image"] != "default.jpg":
            path = os.path.join(IMAGE_FOLDER, product["image"])
            if os.path.exists(path):
                os.remove(path)

        # delete pdf
        for f in ["catalog_pdf", "manual_pdf", "other_pdf"]:
            if product[f]:
                p = os.path.join(PDF_FOLDER, product[f])
                if os.path.exists(p):
                    os.remove(p)

        db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        db.commit()

        return redirect(url_for("products.products_list"))

    finally:
        db.close()


# =========================
# DELETE SINGLE PDF
# =========================
@admin_products_bp.route("/<int:product_id>/delete-pdf/<pdf_type>")
@admin_required
def delete_pdf(product_id, pdf_type):

    db = get_db()

    try:
        product = db.execute("""
            SELECT * FROM products WHERE id = ?
        """, (product_id,)).fetchone()

        if not product:
            abort(404)

        mapping = {
            "catalog": "catalog_pdf",
            "manual": "manual_pdf",
            "other": "other_pdf"
        }

        if pdf_type not in mapping:
            abort(400)

        column = mapping[pdf_type]
        filename = product[column]

        if filename:
            path = os.path.join(PDF_FOLDER, filename)
            if os.path.exists(path):
                os.remove(path)

        db.execute(f"""
            UPDATE products
            SET {column} = NULL
            WHERE id = ?
        """, (product_id,))

        db.commit()

        return redirect(url_for("admin_products.edit", product_id=product_id))

    finally:
        db.close()