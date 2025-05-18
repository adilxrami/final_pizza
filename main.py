from flask import Flask, request, redirect, url_for, session, jsonify, Response
from database import SessionLocal
from crud import OrderService
from models import User, Order, CustomOrder
from utils import login_required
from helpers import get_html_and_css

app = Flask(__name__)
app.secret_key = 'ajf93@FJFF934fjf!FJjf9j3jfJf'
order_service = OrderService()

def encrypt(pw):
    return "".join(chr(ord(c) + 3) for c in pw)

def decrypt(pw):
    return "".join(chr(ord(c) - 3) for c in pw)

@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not all([username, email, phone, password, confirm_password]):
            session['error'] = "All fields are required"
            return redirect(url_for("signup"))

        if password != confirm_password:
            session['error'] = "Passwords do not match"
            return redirect(url_for("signup"))

        if "@" not in email or "." not in email.split("@")[-1] or len(email.split("@")) != 2:
            session['error'] = "Invalid email format"
            return redirect(url_for("signup"))

        if len(password) < 8:
            session['error'] = "Password must be at least 8 characters"
            return redirect(url_for("signup"))

        session_db = SessionLocal()
        if session_db.query(User).filter_by(email=email).first():
            session['error'] = "Email is already registered"
            session_db.close()
            return redirect(url_for("signup"))

        new_user = User(name=username, email=email, phone=phone, password=encrypt(password))
        session_db.add(new_user)
        session_db.commit()
        session_db.close()
        return redirect(url_for("signin"))

    return Response(get_html_and_css("signup", "signup", data={"pagetitle": "Sign Up"}), mimetype="text/html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            session['error'] = "Email and password are required."
            return redirect(url_for("signin"))

        session_db = SessionLocal()
        user = session_db.query(User).filter_by(email=email).first()
        session_db.close()

        if not user or decrypt(user.password) != password:
            session['error'] = "Incorrect email or password."
            return redirect(url_for("signin"))

        session['email'] = user.email
        session['username'] = user.name
        return redirect(url_for('usermenu'))

    return Response(get_html_and_css("signin", "signup", data={"pagetitle": "Sign In"}), mimetype="text/html")

@app.route("/geteror")
def get_error():
    return {"error": session.pop('error', None)}


@login_required
@app.route("/api/user_info")
@login_required
def user_info():
    session_db = SessionLocal()
    user = session_db.query(User).filter_by(email=session.get("email")).first()
    session_db.close()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "username": user.name,
        "email": user.email,
        "phone": user.phone,
        "success": request.args.get("success")
    })


@app.route('/usermenu')
@login_required
def usermenu():
    html_content = get_html_and_css("usermenu", "usermenu", data={"pagetitle": "User Menu"})
    response = Response(html_content, mimetype="text/html")
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response
@login_required
@app.route('/menu')
def menu():
    return Response(get_html_and_css("menu", "menu", data={"pagetitle": "Menu"}), mimetype="text/html")

@app.route('/edit_custom_order/<int:order_id>', methods=['POST'])
@app.route('/edit_custom_order/<int:order_id>', methods=['POST'])
def edit_custom_order(order_id):
    data = request.get_json()
    if not data:
        data = request.form
    session_db = order_service.Session()
    order = session_db.query(CustomOrder).get(order_id)
    if not order:
        session_db.close()
        return redirect(url_for('order_status'))
    order.quantity = int(data.get('quantity', order.quantity))
    order.crust = data.get('crust', order.crust)
    order.cheese = data.get('cheese', order.cheese)
    order.toppings = data.get('toppings', order.toppings)
    order.size = data.get('size', order.size)
    session_db.commit()
    session_db.close()
    return redirect(url_for('order_status'))
@login_required
@app.route('/edit_order/<int:order_id>', methods=['POST'])
def edit_order(order_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    session_db = order_service.Session()
    order = session_db.query(Order).get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.pizza_type = data.get('pizza_type', order.pizza_type)
    order.size = data.get('size', order.size)
    order.crust = data.get('crust', order.crust)
    order.quantity = int(data.get('quantity', order.quantity))
    session_db.commit()
    session_db.close()
    return redirect(url_for('order_status'))
@login_required
@app.route('/order_status')
def order_status():
    return Response(get_html_and_css("order_status", "order_status", data={
        "pagetitle": "Order Status",
        "orders": order_service.get_regular_orders(),
        "custom_orders": order_service.get_custom_orders()
    }), mimetype="text/html")
@login_required
@app.route('/api/orders')
def api_orders():
    return jsonify([
        {
            "id": o.id, "quantity": o.quantity, "size": o.size, 
            "crust": o.crust, "pizza_type": o.pizza_type, 
            "price": float(o.price)
        } for o in order_service.get_regular_orders()
    ])
@login_required
@app.route('/api/custom_orders')
def api_custom_orders():
    return jsonify([
        {
            "id": o.id, "quantity": o.quantity, "size": o.size,
            "crust": o.crust, "cheese": o.cheese,
            "toppings": o.toppings, "price": float(o.price)
        } for o in order_service.get_custom_orders()
    ])

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order_service.delete_order(order_id)
    return redirect(url_for('order_status'))

@app.route('/delete_custom_order/<int:order_id>', methods=['POST'])
def delete_custom_order(order_id):
    order_service.delete_custom_order(order_id)
    return redirect(url_for('order_status'))
@login_required
@app.route('/submit_order', methods=["POST"])
def submit_order():
    email = session.get('email')
    new_order = Order(
        pizza_type=request.form['pizzaType'],
        quantity=int(request.form['quantity']),
        price=request.form['price'],
        size=request.form['size'],
        crust=request.form['crust'],
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin', success="You have been logged out."))
@login_required
@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    session_db = SessionLocal()
    user = session_db.query(User).filter_by(email=session['email']).first()

    if request.method == "POST":
        if decrypt(user.password) != request.form["oldpassword"]:
            return redirect(url_for("edit_profile", error="Old password is incorrect."))

        if request.form["password"] != request.form["confirm_password"]:
            return redirect(url_for("edit_profile", error="New passwords do not match."))

        user.name = request.form["username"]
        user.email = request.form["email"]
        user.phone = request.form["phone"]
        user.password = encrypt(request.form["password"])
        session_db.commit()
        session_db.close()
        return redirect(url_for("edit_profile", success="Profile updated."))

    session_db.close()
    return Response(get_html_and_css("edit_profile", "signup", data={
        "pagetitle": "Edit Profile",
        "error": request.args.get("error"),
        "success": request.args.get("success")
    }), mimetype="text/html")

@app.route('/custom_order', methods=['GET', 'POST'])
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

if __name__ == "__main__":
    app.run(debug=True)
