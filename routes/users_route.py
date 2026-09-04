from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from auth.decorators import admin_required
from models.products import get_products
from models.orders import STATUS_OPTIONS, get_orders, update_order_status
from models.sales import get_sales


users_bp = Blueprint("users", __name__)


@users_bp.get("/")
@admin_required
def dashboard():
    admin = current_user
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
    recent_orders = get_orders()
    for order in recent_orders:
        order["image"] = all_products[order["image_index"]]["image"]
    cart = session.get("cart", [])
    return render_template("dashboard.html", admin=admin, products=products, featured_products=all_products[:3], locations=locations, recent_orders=recent_orders, query=query, cart_count=len(cart))


@users_bp.get("/tienda")
@login_required
def tienda():
    query = request.args.get("q", "").strip()
    all_products = get_products()
    products = [
        product for product in all_products
        if not query or query.lower() in product["name"].lower()
    ]
    cart = session.get("cart", [])
    return render_template("tienda.html", products=products, query=query, cart_count=len(cart))


@users_bp.route("/products/<int:product_id>", methods=["GET", "POST"])
@login_required
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
            cart.append({"product_id": product["id"], "name": product["name"], "price": product["price"], "image": product["image"], "size": selected_size, "color": selected_color})
            session["cart"] = cart
            flash(f"{product['name']} se agrego a tu carrito.", "success")
            return redirect(url_for("users.product_detail", product_id=product_id))

    return render_template("product_detail.html", product=product, cart_count=len(session.get("cart", [])), selected_size=selected_size, selected_color=selected_color)


@users_bp.get("/cart")
@login_required
def cart():
    items = session.get("cart", [])
    total = sum(float(item["price"].replace("$", "").replace(",", "")) for item in items)
    return render_template("cart.html", items=items, total=f"${total:,.2f}")


@users_bp.post("/cart/remove/<int:item_index>")
@login_required
def remove_from_cart(item_index):
    cart_items = session.get("cart", [])
    if 0 <= item_index < len(cart_items):
        removed_item = cart_items.pop(item_index)
        session["cart"] = cart_items
        flash(f"{removed_item['name']} se quito del carrito.", "success")
    return redirect(url_for("users.cart"))


@users_bp.post("/cart/checkout")
@login_required
def checkout():
    if not session.get("cart"):
        flash("Tu carrito esta vacio.", "error")
        return redirect(url_for("users.cart"))
    session.pop("cart")
    flash("Compra finalizada correctamente. Gracias por tu compra.", "success")
    return redirect(url_for("users.cart"))


@users_bp.get("/orders")
@admin_required
def orders():
    selected_status = request.args.get("status", "Todos")
    customer_query = request.args.get("customer", "").strip()
    all_orders = get_orders()
    filtered_orders = [
        order for order in all_orders
        if (selected_status == "Todos" or order["status"] == selected_status)
        and (not customer_query or customer_query.lower() in order["customer"].lower())
    ]
    return render_template("orders.html", orders=filtered_orders, selected_status=selected_status, customer_query=customer_query)


@users_bp.route("/orders/<order_id>", methods=["GET", "POST"])
@admin_required
def order_detail(order_id):
    order = next((item for item in get_orders() if item["id"] == order_id), None)
    if order is None:
        return "Pedido no encontrado", 404
    product = get_products()[order["image_index"]]
    order["image"] = product["image"]
    if request.method == "POST":
        new_status = request.form.get("status")
        if new_status in STATUS_OPTIONS:
            update_order_status(order_id, new_status)
            flash(f"El pedido {order['id']} se actualizo.", "success")
        return redirect(url_for("users.order_detail", order_id=order_id))
    return render_template("order_detail.html", order=order, status_options=STATUS_OPTIONS)


@users_bp.get("/sales")
@admin_required
def sales():
    query = request.args.get("q", "").strip().lower()
    all_sales = get_sales()
    filtered_sales = [
        sale for sale in all_sales
        if not query or any(query in str(sale[field]).lower() for field in ("id", "product", "customer", "status"))
    ]
    total = sum(sale["amount_value"] for sale in filtered_sales)
    successful = sum(1 for sale in filtered_sales if sale["status"] == "Exitoso")
    return render_template(
        "sales.html",
        sales=filtered_sales,
        query=request.args.get("q", "").strip(),
        total=f"${total:,.2f}",
        successful=successful,
    )
