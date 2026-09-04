from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.products import get_products
from models.users import User


users_bp = Blueprint("users", __name__)


@users_bp.get("/")
def dashboard():
    admin = User(name="Alex Rivera", email="admin@pasofirme.com")
    query = request.args.get("q", "").strip()
    all_products = get_products()
    products = [
        product for product in all_products
        if not query or query.lower() in product["name"].lower()
    ]
    locations = [
        {"name": "Singapore", "sales": "$50.45 / 2 months", "change": "+ 2.5%", "trend": "up", "flag": "SG"},
        {"name": "China", "sales": "$199.99 / year", "change": "↓ 2.5%", "trend": "down", "flag": "CN"},
        {"name": "Vietnam", "sales": "$99.99 / month", "change": "+ 2.5%", "trend": "up", "flag": "VN"},
        {"name": "Cambodia", "sales": "$199.99 / year", "change": "+ 2.5%", "trend": "up", "flag": "KH"},
        {"name": "Japan", "sales": "$74.99 / month", "change": "↓ 2.5%", "trend": "down", "flag": "JP"},
    ]
    recent_orders = [
        {"product": "Paris Miki", "customer": "Albert Flores", "amount": "$202.87", "status": "Exitoso", "status_class": "success", "image": all_products[0]["image"]},
        {"product": "Mulberry", "customer": "Jerome Bell", "amount": "$576.28", "status": "Enviando", "status_class": "shipping", "image": all_products[1]["image"]},
        {"product": "JB Martin", "customer": "Theresa Webb", "amount": "$450.54", "status": "Exitoso", "status_class": "success", "image": all_products[2]["image"]},
        {"product": "Ladies Shoes", "customer": "Cody Fisher", "amount": "$354.08", "status": "Exitoso", "status_class": "success", "image": all_products[3]["image"]},
        {"product": "Bally", "customer": "Leslie Alexander", "amount": "$254.08", "status": "Enviando", "status_class": "shipping", "image": all_products[4]["image"]},
    ]
    cart = session.get("cart", [])
    return render_template("dashboard.html", admin=admin, products=products, featured_products=all_products[:3], locations=locations, recent_orders=recent_orders, query=query, cart_count=len(cart))


@users_bp.route("/products/<int:product_id>", methods=["GET", "POST"])
def product_detail(product_id):
    product = next((item for item in get_products() if item["id"] == product_id), None)
    if product is None:
        return "Producto no encontrado", 404

    selected_size = request.form.get("size", "")
    selected_color = request.form.get("color", "")
    if request.method == "POST":
        if selected_size not in product["sizes"] or selected_color not in product["colors"]:
            flash("Selecciona una talla y un color disponibles.", "error")
        else:
            cart = session.get("cart", [])
            cart.append({"product_id": product["id"], "name": product["name"], "price": product["price"], "size": selected_size, "color": selected_color})
            session["cart"] = cart
            flash(f"{product['name']} se agrego a tu carrito.", "success")
            return redirect(url_for("users.product_detail", product_id=product_id))

    return render_template("product_detail.html", product=product, cart_count=len(session.get("cart", [])), selected_size=selected_size, selected_color=selected_color)
