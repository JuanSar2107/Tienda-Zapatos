from flask import Blueprint, render_template

from models.facturas import get_facturas_cliente
from models.pedidos import get_pedidos_cliente
from models.products import get_products
from models.users import get_cliente_actual


users_bp = Blueprint("users", __name__)


@users_bp.get("/")
def dashboard():
    cliente = get_cliente_actual()
    products = get_products()
    return render_template("dashboard.html", cliente=cliente, products=products)


@users_bp.get("/pedidos")
def pedidos():
    cliente = get_cliente_actual()
    return render_template("pedidos.html", cliente=cliente, pedidos=get_pedidos_cliente())


@users_bp.get("/facturas")
def facturas():
    cliente = get_cliente_actual()
    return render_template("facturas.html", cliente=cliente, facturas=get_facturas_cliente())


@users_bp.get("/products/<int:product_id>")
def product_detail(product_id):
    product = next((item for item in get_products() if item["id"] == product_id), None)
    if product is None:
        return "Producto no encontrado", 404
    return render_template("product_detail.html", product=product)
