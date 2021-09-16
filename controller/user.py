from model.user import User
from model.database import Session
from model.result import Result
from model.error import Error
import csv
from sqlalchemy import select


def get_list():
    users_list = []
    with Session() as session:
        statement = select(User)
        users_list = session.execute(statement).scalars().all()
    return users_list


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
        return user_result
    else:
        error = Error(reason="User not found", code=404)

