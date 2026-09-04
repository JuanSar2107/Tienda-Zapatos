from flask import Blueprint, redirect, url_for


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/logout")
def logout():
    return redirect(url_for("users.dashboard"))
