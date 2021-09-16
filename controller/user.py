from model.user import Result
from model.error import Error
from flask import jsonify
import csv
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd


def get_list():
    users_list = []
    with open('res/unique_party_rk.csv', newline='') as users:
        reader = csv.DictReader(users, fieldnames=["party_rk"])
        pool = ThreadPool(4)
        users_list = list(pool.map(lambda x: x["party_rk"], reader))
        pool.close()
        users_list.pop(0)
    return jsonify(users_list)


def get_result_by(user_id):
    user_result = None
    with open('res/1_month.csv', newline='') as csv_doc:
        reader = csv.DictReader(csv_doc)
        user_result = list(
            filter(lambda row: row["party_rk"] == user_id, reader)
        )
    if user_result:
        user_result = list(
            map(
                lambda u: Result(
                    id=u["party_rk"],
                    predicted_sum=u["pred_sum"],
                    real_sum=u["real_sum"],
                    category=u["category"],
                    month=u["month"]
                ),
                user_result
            )
        )

        user_result = sorted(
            user_result, key=lambda x: x.predicted_sum, reverse=True
        )
        cashback = { res.category : 5 for res in user_result }
        print(cashback)
        return jsonify(user_result)
    else:
        error = Error(reason="User not found", code=404)

