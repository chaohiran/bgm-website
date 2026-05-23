from flask import Blueprint, render_template, request, redirect, session, url_for

admin_auth_bp = Blueprint("admin_auth", __name__)

<<<<<<< HEAD
# 🔑 simple admin (ตอนนี้ยัง basic)
=======
# 🔑 ตั้งค่า user (เริ่มแบบง่ายก่อน)
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf
ADMIN_USER = "admin"
ADMIN_PASS = "1234"


<<<<<<< HEAD
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
=======
@admin_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("home.index"))
        else:
            error = "Username or Password incorrect"
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf

    return render_template("admin/login.html", error=error)


<<<<<<< HEAD
# =========================
# 🚪 LOGOUT
# =========================
@admin_auth_bp.route("/logout")
def logout():

    # 🔥 ล้าง session ทั้งหมด (ปลอดภัยกว่า pop)
    session.clear()

    # กลับไปหน้า login
=======
@admin_auth_bp.route("/logout")
def logout():
    session.pop("admin", None)
>>>>>>> f6667076cc1645c66d4d6232231fce5bb9f97cdf
    return redirect(url_for("admin_auth.login"))