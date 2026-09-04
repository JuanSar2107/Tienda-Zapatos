from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user, login_required


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            flash("No tienes permisos para acceder a esa seccion.", "danger")
            return redirect(url_for("users.tienda"))
        return view(*args, **kwargs)

    return wrapped
