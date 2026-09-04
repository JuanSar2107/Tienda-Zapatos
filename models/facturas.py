from models.pedidos import get_pedidos_cliente


def get_facturas_cliente():
    facturas = []

    for pedido in get_pedidos_cliente():
        pagada = pedido["status"] != "Pendiente"
        facturas.append({
            "id": f"F-{1000 + pedido['id']}",
            "product": pedido["product"],
            "date": pedido["date"],
            "amount": pedido["price"],
            "status": "Pagada" if pagada else "Pendiente",
            "status_class": "success" if pagada else "pending",
        })

    return facturas
