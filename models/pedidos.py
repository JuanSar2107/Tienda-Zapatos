from models.products import get_products


def get_pedidos_cliente():
    products = get_products()

    return [
        {"id": 1, "product": products[0]["name"], "image": products[0]["image"], "size": "40", "color": "Rojo", "price": "$106.58", "quantity": 1, "date": "2026-08-02", "status": "Entregado", "status_class": "success"},
        {"id": 2, "product": products[2]["name"], "image": products[2]["image"], "size": "39", "color": "Gris", "price": "$189.99", "quantity": 1, "date": "2026-08-15", "status": "Enviando", "status_class": "shipping"},
        {"id": 3, "product": products[4]["name"], "image": products[4]["image"], "size": "36", "color": "Blanco", "price": "$248.55", "quantity": 2, "date": "2026-08-20", "status": "Pendiente", "status_class": "pending"},
    ]
