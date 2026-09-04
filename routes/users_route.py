from flask import Blueprint, render_template

from models.users import User


users_bp = Blueprint("users", __name__)


@users_bp.get("/")
def dashboard():
    admin = User(name="Alex Rivera", email="admin@pasofirme.com")
    stats = [
        {"label": "Ventas del mes", "value": "$24,680", "change": "+12.8%", "trend": "up", "icon": "chart"},
        {"label": "Pedidos pendientes", "value": "38", "change": "+4.2%", "trend": "up", "icon": "bag"},
        {"label": "Productos activos", "value": "486", "change": "+18 nuevos", "trend": "neutral", "icon": "box"},
        {"label": "Clientes registrados", "value": "2,840", "change": "+8.5%", "trend": "up", "icon": "users"},
    ]
    recent_orders = [
        {"id": "#ZP-1048", "customer": "Sofia Martinez", "product": "Air Runner White", "amount": "$129.00", "status": "En preparacion", "status_class": "preparing", "initials": "SM"},
        {"id": "#ZP-1047", "customer": "Carlos Ramirez", "product": "Urban Leather Black", "amount": "$189.00", "status": "Enviado", "status_class": "shipped", "initials": "CR"},
        {"id": "#ZP-1046", "customer": "Laura Torres", "product": "Cloud Walk Sand", "amount": "$99.00", "status": "Entregado", "status_class": "delivered", "initials": "LT"},
        {"id": "#ZP-1045", "customer": "Diego Herrera", "product": "Street High Canvas", "amount": "$115.00", "status": "Pendiente", "status_class": "pending", "initials": "DH"},
    ]
    return render_template("dashboard.html", admin=admin, stats=stats, recent_orders=recent_orders)
