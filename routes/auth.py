from flask import Blueprint, redirect, session, url_for


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("users.dashboard"))
