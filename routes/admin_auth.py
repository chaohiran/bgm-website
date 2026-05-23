from flask import Blueprint, render_template, request, redirect, session, url_for

admin_auth_bp = Blueprint("admin_auth", __name__)

ADMIN_USER = "admin"
ADMIN_PASS = "1234"


@admin_auth_bp.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username") or ""
        password = request.form.get("password") or ""

        username = username.strip()
        password = password.strip()

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("home.index"))
        else:
            error = "Username หรือ Password ไม่ถูกต้อง"

    return render_template("admin/login.html", error=error)


@admin_auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("admin_auth.login"))