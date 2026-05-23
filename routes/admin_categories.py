from flask import Blueprint, render_template, request, redirect, url_for, abort
from database import get_db
from utils.admin_guard import admin_required

import os
import uuid

admin_categories_bp = Blueprint(
    "admin_categories",
    __name__,
    url_prefix="/admin/categories"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "static", "img", "categories")
UPLOAD_FOLDER = os.path.normpath(UPLOAD_FOLDER)


# =========================
# 📂 LIST CATEGORIES
# =========================
@admin_categories_bp.route("/")
@admin_required
def index():

    db = get_db()
    categories = db.execute("""
        SELECT * FROM categories ORDER BY id ASC
    """).fetchall()
    db.close()

    return render_template(
        "products.html",
        categories=categories
    )


# =========================
# ✏️ EDIT CATEGORY
# =========================
@admin_categories_bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(category_id):

    db = get_db()

    category = db.execute(
        "SELECT * FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()

    if not category:
        db.close()
        abort(404)

    if request.method == "POST":

        # ✅ SAFE ACCESS (sqlite3.Row ไม่มี .get)
        name_th = request.form.get("name_th") or category["name_th"]
        name_en = request.form.get("name_en") or category["name_en"]

        key = request.form.get("key") or category["key"]

        image = category["image"]

        file = request.files.get("image")

        if file and file.filename:

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # ลบรูปเก่า
            if image:
                old_path = os.path.join(UPLOAD_FOLDER, image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            ext = file.filename.rsplit(".", 1)[-1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            image = filename

        db.execute("""
            UPDATE categories
            SET name_th = ?, name_en = ?, key = ?, image = ?
            WHERE id = ?
        """, (name_th, name_en, key, image, category_id))

        db.commit()
        db.close()

        return redirect(url_for("admin_categories.index"))

    db.close()

    return render_template("admin/categories/edit.html", category=category)

@admin_categories_bp.route("/<int:category_id>/delete")
@admin_required
def delete(category_id):

    db = get_db()

    category = db.execute(
        "SELECT * FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()

    if not category:
        db.close()
        abort(404)

    if category["image"]:
        path = os.path.join(UPLOAD_FOLDER, category["image"])
        if os.path.exists(path):
            os.remove(path)

    db.execute("DELETE FROM categories WHERE id = ?", (category_id,))

    db.commit()
    db.close()

    return redirect(url_for("admin_categories.index"))

@admin_categories_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():

    db = get_db()

    if request.method == "POST":

        name_th = request.form.get("name_th")
        name_en = request.form.get("name_en")
        key = request.form.get("key")

        image = None

        file = request.files.get("image")

        if file and file.filename:

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            ext = file.filename.rsplit(".", 1)[-1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            image = filename

        db.execute("""
            INSERT INTO categories (name_th, name_en, key, image)
            VALUES (?, ?, ?, ?)
        """, (name_th, name_en, key, image))

        db.commit()
        db.close()

        return redirect(url_for("admin_categories.index"))

    db.close()

    return render_template("admin/categories/create.html")