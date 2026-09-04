from flask import Blueprint, render_template

from models.products import get_products
from models.users import User


users_bp = Blueprint("users", __name__)


@users_bp.get("/")
def dashboard():
    admin = User(name="Alex Rivera", email="admin@pasofirme.com")
    products = get_products()
    locations = [
        {"name": "Singapore", "sales": "$50.45 / 2 months", "change": "+ 2.5%", "trend": "up", "flag": "SG"},
        {"name": "China", "sales": "$199.99 / year", "change": "↓ 2.5%", "trend": "down", "flag": "CN"},
        {"name": "Vietnam", "sales": "$99.99 / month", "change": "+ 2.5%", "trend": "up", "flag": "VN"},
        {"name": "Cambodia", "sales": "$199.99 / year", "change": "+ 2.5%", "trend": "up", "flag": "KH"},
        {"name": "Japan", "sales": "$74.99 / month", "change": "↓ 2.5%", "trend": "down", "flag": "JP"},
    ]
    recent_orders = [
        {"product": "Paris Miki", "customer": "Albert Flores", "amount": "$202.87", "status": "Exitoso", "status_class": "success", "image": products[0]["image"]},
        {"product": "Mulberry", "customer": "Jerome Bell", "amount": "$576.28", "status": "Enviando", "status_class": "shipping", "image": products[1]["image"]},
        {"product": "JB Martin", "customer": "Theresa Webb", "amount": "$450.54", "status": "Exitoso", "status_class": "success", "image": products[2]["image"]},
        {"product": "Ladies Shoes", "customer": "Cody Fisher", "amount": "$354.08", "status": "Exitoso", "status_class": "success", "image": products[3]["image"]},
        {"product": "Bally", "customer": "Leslie Alexander", "amount": "$254.08", "status": "Enviando", "status_class": "shipping", "image": products[4]["image"]},
    ]
    return render_template("dashboard.html", admin=admin, products=products, locations=locations, recent_orders=recent_orders)


@users_bp.get("/products/<int:product_id>")
def product_detail(product_id):
    product = next((item for item in get_products() if item["id"] == product_id), None)
    if product is None:
        return "Producto no encontrado", 404
    return render_template("product_detail.html", product=product)
