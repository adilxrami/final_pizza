from flask import Blueprint, request, session, redirect, url_for, jsonify, Response
from database import SessionLocal
from crud import OrderService
from models import Order, CustomOrder
from utils import login_required
from helpers import get_html_and_css

order_bp = Blueprint("orders", __name__)
order_service = OrderService()


@order_bp.route('/usermenu')
@login_required
def usermenu():
    html_content = get_html_and_css("usermenu", "usermenu", data={"pagetitle": "User Menu"})
    response = Response(html_content, mimetype="text/html")
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response


@order_bp.route('/menu')
@login_required
def menu():
    return Response(get_html_and_css("menu", "menu", data={"pagetitle": "Menu"}), mimetype="text/html")


@order_bp.route('/submit_order', methods=["POST"])
@login_required
def submit_order():
    email = session.get('email')
    new_order = Order(
        pizza_type=request.form['pizzaType'],
        quantity=int(request.form['quantity']),
        price=request.form['price'],
        size=request.form['size'],
        crust=request.form['crust'],
        cheese=request.form['cheese'],
        email=email
    )
    session_db = SessionLocal()
    session_db.add(new_order)
    session_db.commit()
    session_db.close()

    return Response(get_html_and_css("order_success", "order_success", data={
        "pagetitle": "Order Success",
        "message": "Order submitted successfully!"
    }), mimetype="text/html")

@order_bp.route('/edit_order/<int:order_id>', methods=['POST'])
@login_required
def edit_order(order_id):
    data = request.get_json()
    if not data:
        data = request.form

    session_db = order_service.Session()
    order = session_db.query(Order).get(order_id)
    if not order:
        session_db.close()
        return redirect(url_for('orders.order_status'))

    order.pizza_type = data.get('pizza_type', order.pizza_type)
    order.size = data.get('size', order.size)
    order.crust = data.get('crust', order.crust)
    order.cheese = data.get('cheese', order.cheese)

    try:
        order.quantity = int(data.get('quantity', order.quantity))
        if order.quantity < 1:
            order.quantity = 1
    except (ValueError, TypeError):
        order.quantity = order.quantity

    base_prices = {
        'margherita': 8,
        'pepperoni': 10,
        'bbq_chicken': 12,
        'veggie': 9
    }
    size_prices = {
        'small': 0,
        'medium': 2,
        'large': 4
    }
    crust_prices = {
        'thin': 0,
        'thick': 1,
        'stuffed': 2
    }
    cheese_prices = {
        'mozzarella': 1,
        'cheddar': 1.5,
        'parmesan': 2,
        'none': 0
    }

    base_price = base_prices.get(order.pizza_type, 0)
    size_price = size_prices.get(order.size, 0)
    crust_price = crust_prices.get(order.crust, 0)
    cheese_price = cheese_prices.get(order.cheese, 0)

    total_price = (base_price + size_price + crust_price + cheese_price) * order.quantity
    order.price = round(total_price, 2)

    session_db.commit()
    session_db.close()

    return redirect(url_for('orders.order_status'))

@order_bp.route('/custom_order', methods=['GET', 'POST'])
@login_required
def custom_order():
    if request.method == 'POST':
        size = request.form.get('size')
        crust = request.form.get('crust')
        cheese = request.form.get('cheese')
        toppings = request.form.getlist('toppings')
        quantity = int(request.form.get('quantity', 1))
        email = session.get('email')

        base_price = float(size) + float(cheese)
        base_price += sum(1 if t in ['pepperoni', 'sausage', 'bacon'] else 0.5 for t in toppings)
        total_price = round(base_price * quantity, 2)

        new_order = CustomOrder(
            size=size, crust=crust, cheese=cheese,
            toppings=", ".join(toppings), price=total_price,
            quantity=quantity, email=email
        )

        session_db = SessionLocal()
        session_db.add(new_order)
        session_db.commit()
        session_db.close()

        return Response(get_html_and_css("order_success", "order_success", data={
            "pagetitle": "Order Success",
            "message": "Order submitted successfully!",
            "total": total_price
        }), mimetype="text/html")

    return Response(get_html_and_css("custom_order", "custom_order", data={"pagetitle": "Custom Order"}), mimetype="text/html")


@order_bp.route('/order_status')
@login_required
def order_status():
    return Response(get_html_and_css("order_status", "order_status", data={
        "pagetitle": "Order Status",
        "orders": order_service.get_regular_orders(),
        "custom_orders": order_service.get_custom_orders()
    }), mimetype="text/html")


@order_bp.route('/api/orders')
@login_required
def api_orders():
    return jsonify([
        {
            "id": o.id, "quantity": o.quantity, "size": o.size, 
            "crust": o.crust, "pizza_type": o.pizza_type, 
            "price": float(o.price)
        } for o in order_service.get_regular_orders()
    ])


@order_bp.route('/api/custom_orders')
@login_required
def api_custom_orders():
    return jsonify([
        {
            "id": o.id, "quantity": o.quantity, "size": o.size,
            "crust": o.crust, "cheese": o.cheese,
            "toppings": o.toppings, "price": float(o.price)
        } for o in order_service.get_custom_orders()
    ])
@order_bp.route('/edit_custom_order/<int:order_id>', methods=['POST'])
@login_required
def edit_custom_order(order_id):
    data = request.get_json()
    if not data:
        data = request.form

    session_db = order_service.Session()
    order = session_db.query(CustomOrder).get(order_id)
    if not order:
        session_db.close()
        return redirect(url_for('orders.order_status'))

    order.size = data.get('size', order.size)
    order.crust = data.get('crust', order.crust)
    order.cheese = data.get('cheese', order.cheese)
    order.toppings = data.get('toppings', order.toppings)
    order.quantity = int(data.get('quantity', order.quantity))
    cheese_prices = {
        "0": 0,
        "1": 1,
        "1.5": 1.5,
        "2": 2
    }

    try:
        cheese_price = cheese_prices.get(str(order.cheese), 0)
    except Exception:
        cheese_price = 0

    toppings_list = [t.strip() for t in order.toppings.split(',') if t.strip()]
    toppings_count = len(toppings_list)

    base_price = 10

    total_price = (base_price + cheese_price + toppings_count * 1) * order.quantity
    order.price = round(total_price, 2)

    session_db.commit()
    session_db.close()

    return redirect(url_for('orders.order_status'))

@order_bp.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    order_service.delete_order(order_id)
    return redirect(url_for('orders.order_status'))


@order_bp.route('/delete_custom_order/<int:order_id>', methods=['POST'])
@login_required
def delete_custom_order(order_id):
    order_service.delete_custom_order(order_id)
    return redirect(url_for('orders.order_status'))
