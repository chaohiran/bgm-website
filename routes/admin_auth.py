from flask import Blueprint, render_template, request, redirect, session, url_for

admin_auth_bp = Blueprint("admin_auth", __name__)

# 🔑 simple admin (ตอนนี้ยัง basic)
ADMIN_USER = "admin"
ADMIN_PASS = "1234"


# =========================
# 🔐 LOGIN
# =========================
@admin_auth_bp.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        if username == ADMIN_USER and password == ADMIN_PASS:

            # ✅ mark admin session
            session["admin"] = True

            # 🔥 redirect ไป admin dashboard จริง
            return redirect(url_for("home.index"))

        else:
            error = "Username หรือ Password ไม่ถูกต้อง"

    return render_template("admin/login.html", error=error)


# =========================
# 🚪 LOGOUT
# =========================
@admin_auth_bp.route("/logout")
def logout():

    # 🔥 ล้าง session ทั้งหมด (ปลอดภัยกว่า pop)
    session.clear()

    # กลับไปหน้า login
    return redirect(url_for("admin_auth.login"))