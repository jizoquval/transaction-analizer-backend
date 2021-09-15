from model.cashback import Cashback
from model.error import Error
from model.user import User
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

users = [User(id = "23", result=17), User(id = "12", result=88)]
cashback = Cashback(persent = 0)

@app.route('/')
def index():
  return "<h1>Welcome!</h1>"

@app.route("/user/list")
def get_users():
    return jsonify(users)

@app.route("/user/result/<string:user_id>")
def get_result_for(user_id):
    result = next((user for user in users if user.id == user_id), None)
    if result:
        return f'result: {result.result}'
    else:
        error = Error(reason="User not found", code=404)
        return jsonify(error), error.code

@app.route("/cashback", methods=['GET', 'POST'])
def set_cashback_persents():
    if request.method == "POST":
        args = request.args
        newValue = args.get("value", None)
        if newValue:
            global cashback
            cashback = Cashback(persent = newValue)
            return f'SET NEW VALUE CASHBACK {newValue}'
        else:
            error = Error(reason="missed arg :value", code = 400)
            return jsonify(error.reason), error.code
    else: 
        return jsonify(cashback)

@app.route("/metrics")
def get_metrics():
    args = request.args
    month = args.get("month", None)
    if month:
        return f'get metrics for all users by months {month}'
    else:
         return "get metrics for all users"
