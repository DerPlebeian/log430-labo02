"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from collections import defaultdict

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()

    orders = []
    for key in r.scan_iter("order:*"):
        order_data = r.hgetall(key)
        orders.append(order_data)

        if len(orders) >= limit:
            break

    return orders

def get_highest_spending_users():
    """Get report of highest spending users"""
    orders = get_orders_from_redis(99)
    expenses_by_user = defaultdict(float)

    for order in orders:
        user_id = order.get("user_id")
        total_amount = float(order.get("total_amount", 0))
        expenses_by_user[user_id] += total_amount

    highest_spending_users = sorted(expenses_by_user.items(), key=lambda item: item[1], reverse=True)
    return highest_spending_users

def get_highest_spending_products():
    """Get report of best selling products"""
    r = get_redis_conn()

    products_sold = []
    for key in r.scan_iter("product:*"):
        product_id = key.split(":")[1]
        quantity_sold = int(r.get(key) or 0)
        products_sold.append((product_id, quantity_sold))

    return sorted(products_sold, key=lambda item: item[1], reverse=True)