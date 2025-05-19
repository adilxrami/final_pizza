from flask import Flask
from auth import auth
from order_routes import order_bp
from helpers import get_html_and_css  

app = Flask(__name__)
app.secret_key = 'ajf93@FJFF934fjf!FJjf9j3jfJf'

app.register_blueprint(auth)
app.register_blueprint(order_bp)

@app.errorhandler(404)
def not_found(e):
    return get_html_and_css("404", "error", data={"pagetitle": "Not Found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
