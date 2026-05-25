from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
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

UPLOAD_FOLDER = os.path.normpath(
    os.path.join(BASE_DIR, "..", "static", "img", "categories")
)


# =========================
# 📂 LIST CATEGORIES
# =========================
@admin_categories_bp.route("/")
@admin_required
def index():

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
# ➕ CREATE CATEGORY
# =========================
@admin_categories_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():

    db = get_db()

    if request.method == "POST":

        name_th = (request.form.get("name_th") or "").strip()
        name_en = (request.form.get("name_en") or "").strip()
        key = (request.form.get("key") or "").strip()

        # validation
        if not name_th or not name_en or not key:
            db.close()
            return "กรุณากรอกข้อมูลให้ครบ", 400

        # duplicate check
        existing = db.execute("""
            SELECT id FROM categories WHERE key = ?
        """, (key,)).fetchone()

        if existing:
            db.close()
            return "Category key already exists", 400

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


# =========================
# ✏️ EDIT CATEGORY
# =========================
@admin_categories_bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(category_id):

    db = get_db()

    category = db.execute("""
        SELECT * FROM categories WHERE id = ?
    """, (category_id,)).fetchone()

    if not category:
        db.close()
        abort(404)

    if request.method == "POST":

        name_th = (request.form.get("name_th") or category["name_th"]).strip()
        name_en = (request.form.get("name_en") or category["name_en"]).strip()
        key = (request.form.get("key") or category["key"]).strip()

        image = category["image"]

        file = request.files.get("image")

        if file and file.filename:

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # delete old image
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

    return render_template(
        "admin/categories/edit.html",
        category=category
    )


# =========================
# 🗑 DELETE CATEGORY
# =========================
@admin_categories_bp.route("/<int:category_id>/delete")
@admin_required
def delete(category_id):

    db = get_db()

    category = db.execute("""
        SELECT * FROM categories WHERE id = ?
    """, (category_id,)).fetchone()

    if not category:
        db.close()
        abort(404)

    if category["image"]:
        path = os.path.join(UPLOAD_FOLDER, category["image"])
        if os.path.exists(path):
            os.remove(path)

    db.execute("""
        DELETE FROM categories WHERE id = ?
    """, (category_id,))

    db.commit()
    db.close()

    return redirect(url_for("admin_categories.index"))

# =========================
# SAVE CATEGORY ORDER
# =========================
@admin_categories_bp.route("/save-order", methods=["POST"])
@admin_required
def save_order():

    data = request.get_json()

    ids = data.get("ids", [])

    db = get_db()

    for index, category_id in enumerate(ids):

        db.execute("""
            UPDATE categories
            SET sort_order = ?
            WHERE id = ?
        """, (
            index + 1,
            category_id
        ))

    db.commit()
    db.close()

    return jsonify({
        "success": True
    })