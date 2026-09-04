ORDERS = [
    {"id": "ZS-1048", "product": "Paris Miki", "customer": "Albert Flores", "email": "albert@example.com", "amount": "$202.87", "status": "Exitoso", "status_class": "success", "image_index": 0, "date": "04 Sep 2026", "location": "Ciudad de Mexico", "address": "Av. Reforma 120, Ciudad de Mexico"},
    {"id": "ZS-1047", "product": "Mulberry", "customer": "Jerome Bell", "email": "jerome@example.com", "amount": "$576.28", "status": "Enviando", "status_class": "shipping", "image_index": 1, "date": "03 Sep 2026", "location": "Bogota", "address": "Calle 72 #14-20, Bogota"},
    {"id": "ZS-1046", "product": "JB Martin", "customer": "Theresa Webb", "email": "theresa@example.com", "amount": "$450.54", "status": "Exitoso", "status_class": "success", "image_index": 2, "date": "02 Sep 2026", "location": "Sao Paulo", "address": "Rua Augusta 850, Sao Paulo"},
    {"id": "ZS-1045", "product": "Ladies Shoes", "customer": "Cody Fisher", "email": "cody@example.com", "amount": "$354.08", "status": "Pendiente", "status_class": "pending", "image_index": 3, "date": "01 Sep 2026", "location": "Barcelona", "address": "Carrer de Valencia 25, Barcelona"},
    {"id": "ZS-1044", "product": "Bally", "customer": "Leslie Alexander", "email": "leslie@example.com", "amount": "$254.08", "status": "Enviando", "status_class": "shipping", "image_index": 4, "date": "31 Ago 2026", "location": "Sao Paulo", "address": "Rua Oscar Freire 60, Sao Paulo"},
]


STATUS_OPTIONS = {
    "Pendiente": "pending",
    "Enviando": "shipping",
    "Exitoso": "success",
}


def get_orders():
    return [order.copy() for order in ORDERS]


def update_order_status(order_id, status):
    for order in ORDERS:
        if order["id"] == order_id and status in STATUS_OPTIONS:
            order["status"] = status
            order["status_class"] = STATUS_OPTIONS[status]
            return True
    return False
