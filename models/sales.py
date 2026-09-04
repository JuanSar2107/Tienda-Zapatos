from models.orders import get_orders


def get_sales():
    sales = []
    for order in get_orders():
        amount = float(order["amount"].replace("$", "").replace(",", ""))
        sale = order.copy()
        sale["amount_value"] = amount
        sales.append(sale)
    return sales
