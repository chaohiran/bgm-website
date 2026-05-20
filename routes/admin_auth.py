from flask import Blueprint, render_template, request, redirect, session, url_for

admin_auth_bp = Blueprint("admin_auth", __name__)

# 🔑 ตั้งค่า user (เริ่มแบบง่ายก่อน)
ADMIN_USER = "admin"
ADMIN_PASS = "1234"


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

    return render_template("admin/login.html", error=error)


@admin_auth_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin_auth.login"))