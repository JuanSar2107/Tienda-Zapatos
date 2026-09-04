from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from auth import db
from auth.models import User
from roles import USER_ROLE

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


def _home_for(usuario):
    return url_for("users.dashboard") if usuario.is_admin else url_for("users.tienda")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(_home_for(current_user))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirmar = request.form.get("confirmar", "")

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.", "danger")
        elif password != confirmar:
            flash("Las contraseñas no coinciden.", "danger")
        elif len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Ya existe una cuenta con ese correo.", "danger")
        else:
            usuario = User(nombre=nombre, email=email, role=USER_ROLE)
            usuario.set_password(password)
            db.session.add(usuario)
            db.session.commit()
            flash("Cuenta creada correctamente. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(_home_for(current_user))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        recordarme = bool(request.form.get("recordarme"))

        usuario = User.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            login_user(usuario, remember=recordarme)
            siguiente = request.args.get("next")
            flash(f"Bienvenido, {usuario.nombre}.", "success")
            return redirect(siguiente or _home_for(usuario))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
