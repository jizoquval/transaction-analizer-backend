from model.user import User
from controller.setup_data import set_inital_data
import os
from model.cashback_category import Category
from model.database import DATABASE_NAME, Session, create_db
from controller.metrics import check_same_cashback_persent, metric_business_all_users, metric_business_all_users_aproximate, metric_business_selected_users
from model.error import Error
from quart import Quart, jsonify, request
from quart_cors import cors, route_cors
from controller import user as user_controller
import pandas as pd
from sqlalchemy import select, update, func

app = Quart(__name__)
app = cors(app, allow_origin="*",
           allow_headers=["Content-Type"], allow_methods=['GET', 'POST'])

if not os.path.exists(DATABASE_NAME):
    create_db()
    set_inital_data()


@app.route("/user/list")
async def get_users():
    return jsonify(user_controller.get_list())


@app.route("/user/result/<string:user_id>")
async def get_result_for(user_id):
    return jsonify(user_controller.get_result_by(user_id))


@app.route("/cashback")
async def get_cashback_persents():
    with Session() as session:
        statement = select(Category)
        cashback_categories = session.execute(statement).scalars().all()
        return jsonify(cashback_categories)


@app.route("/cashback/set")
async def set_cashback_persents():
    with Session() as session:
        args = request.args
        newValue = args.get("value", None)
        category = args.get("category", None)
        if newValue:
            if category:
                session.query(Category).filter(Category.name == category).update(
                    {Category.cashback: newValue}
                )
                session.commit()
                return {'msg': f'Set new cashback {newValue} for {category}'}
            else:
                session.query(Category).update(
                    {Category.cashback: newValue}
                )
                session.commit()
                return {'msg': f'Set new cashback for all categories {newValue}'}
        else:
            error = Error(reason="missed arg :value", code=400)
            return jsonify(error.reason), error.code


@app.route("/metrics")
async def get_metrics():
    args = request.args
    month = int(args.get("month", None))
    user_id = args.get("user_id", None)
    if month:
        if not (month == 1 or month == 2):
            error = Error("month can be 1 or 2", 400)
            return jsonify(error.reason), error.code

        with Session() as session:
            data = pd.read_csv(f'res/{month}_month.csv')
            statement = select(Category.name, Category.cashback)
            cashback_categories = dict(session.execute(statement).all())
            if user_id:
                # get metrics for user {user_id} by months {month}
                users = user_controller.get_list()
                value = metric_business_selected_users(
                    data, cashback_categories, [int(user_id)]
                )
                return jsonify(value)
            else:
                # get metrics for all users by months {month}
                statement = session.query(func.count(User.party_rk))
                users_count = session.execute(statement).scalars().one()
                value = await metric_business_all_users(
                    data, cashback_categories, users_count
                )
                return jsonify(value)
    else:
        error = Error("specify arg month", 400)
        return jsonify(error.reason), error.code


@app.route("/metrics_average")
async def get_average_metrics():
    args = request.args
    month = int(args.get("month", None))
    users_count = int(args.get("users_count", 4000))

    if month:
        if not (month == 1 or month == 2):
            error = Error("month can be 1 or 2", 400)
            return jsonify(error.reason), error.code
        with Session() as session:
            data = pd.read_csv(f'res/{month}_month.csv')
            users = pd.read_csv(f'res/unique_party_rk.csv')
            statement = select(Category.name, Category.cashback)
            cashback_categories = dict(session.execute(statement).all())

            return metric_business_all_users_aproximate(data, users, cashback_categories, users_count)
    else:
        error = Error("specify arg month", 400)
        return jsonify(error.reason), error.code