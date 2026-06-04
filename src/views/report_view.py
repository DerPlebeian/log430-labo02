"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param
from controllers.order_controller import get_report_highest_spending_users, get_report_best_sellers

def show_highest_spending_users():
    """ Show report of highest spending users """
    highest_spending_users = get_report_highest_spending_users()

    rows = [
        f"<li>Utilisateur {user_id}: ${total_spent:.2f}</li>"
        for user_id, total_spent in highest_spending_users
    ]

    if not rows:
        rows = ["<li>Aucune donnée disponible</li>"]

    return get_template(f"""
        <h2>Les plus gros acheteurs</h2>
        <ul>
            {" ".join(rows)}
        </ul>
    """)

def show_best_sellers():
    """ Show report of best selling products """
    best_sellers = get_report_best_sellers()

    rows = [
        f"<li>Article {product_id}: {quantity_sold} vendu(s)</li>"
        for product_id, quantity_sold in best_sellers
    ]

    if not rows:
        rows = ["<li>Aucune donnée disponible</li>"]

    return get_template(f"""
        <h2>Les articles les plus vendus</h2>
        <ul>
            {" ".join(rows)}
        </ul>
    """)