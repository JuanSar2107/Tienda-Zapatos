from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.users import create_user, get_user_by_email


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        user = get_user_by_email(email)
        if user is None or not user.check_password(password):
            flash("Correo o contrasena incorrectos.")
            return redirect(url_for("auth.login"))

        session["user_email"] = user.email
        return redirect(url_for("users.dashboard"))

    return render_template("login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if get_user_by_email(email):
            flash("Ese correo ya esta registrado.")
            return redirect(url_for("auth.registro"))

        create_user(name=name, email=email, password=password)
        flash("Cuenta creada correctamente, ya puedes iniciar sesion.")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.get("/logout")
def logout():
    session.pop("user_email", None)
    return redirect(url_for("auth.login"))
