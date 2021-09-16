from controller.metrics import metric_business_all_users, metric_business_selected_users
from model.error import Error
from flask import Flask, jsonify
from flask import request
from controller import user as user_controller
import pandas as pd

app = Flask(__name__)

categories = ['Финансовые услуги', 'Наличные', 'Разные товары', 'Транспорт',
'Супермаркеты', 'Фаст Фуд', 'Топливо', 'Связь/Телеком',
'Дом/Ремонт', 'Животные', 'Рестораны', 'Сувениры', 'Аренда авто',
'Медицинские услуги', 'Турагентства', 'Спорттовары', 'Аптеки',
'Цветы', 'Госсборы', 'Одежда/Обувь', 'Книги', 'Музыка', 'Красота',
'Сервисные услуги', 'Кино', 'Авиабилеты', 'Частные услуги',
'Развлечения', 'НКО', 'Автоуслуги', 'Отели', 'Ж/д билеты',
'Образование', 'Искусство', 'Фото/Видео', 'Duty Free']

cashbacks = dict()

for cat in categories:
    cashbacks[cat] = 0.05

# cashbacks = {'Финансовые услуги': 5, 'Одежда/Обувь': 5, 'Разные товары': 5, 'Супермаркеты': 5, 'Красота': 5, 'Сувениры': 5, 'Фаст Фуд': 5, 'Дом/Ремонт': 5, 'Сервисные услуги': 5, 'Транспорт': 5, 'Медицинские услуги': 5, 'Топливо': 5, 'Наличные': 5, 'Связь/Телеком': 5, 'Частные услуги': 5, 'Рестораны': 5,
#              'Развлечения': 5, 'НКО': 5, 'Книги': 5, 'Кино': 5, 'Автоуслуги': 5, 'Музыка': 5, 'Отели': 5, 'Аптеки': 5, 'Цветы': 5, 'Ж/д билеты': 5, 'Авиабилеты': 5, 'Спорттовары': 5, 'Госсборы': 5, 'Аренда авто': 5, 'Животные': 5, 'Duty Free': 5, 'Турагентства': 5, 'Образование': 5, 'Искусство': 5, 'Фото/Видео': 5}


@app.route('/')
def index():
    return "<h1>Welcome!</h1>"


@app.route("/user/list")
def get_users():
    return jsonify(user_controller.get_list())


@app.route("/user/result/<string:user_id>")
def get_result_for(user_id):
    return jsonify(user_controller.get_result_by(user_id))


@app.route("/cashback", methods=['GET', 'POST'])
def set_cashback_persents():
    if request.method == "POST":
        args = request.args
        newValue = args.get("value", None)
        category = args.get("category", None)
        if newValue:
            if category:
                cashbacks[category] = newValue
                return f'Set new cashback {newValue} for {category}'
            else:
                for key in cashbacks.keys():
                    cashbacks[key] = newValue
                return f'Set new cashback for all categories {newValue}'
        else:
            error = Error(reason="missed arg :value", code=400)
            return jsonify(error.reason), error.code
    else:
        return jsonify(cashbacks)


@app.route("/metrics")
def get_metrics():
    args = request.args
    month = args.get("month", None)
    user_id = args.get("user_id", None)
    if month:
        data = pd.read_csv(f'res/{month}_month.csv')
        if user_id:
            # get metrics for user {user_id} by months {month}
            users = user_controller.get_list()
            value = metric_business_selected_users(data, cashbacks, [int(user_id)])
            return jsonify(value) 
        else:
            # get metrics for all users by months {month}
            value = metric_business_all_users(data, cashbacks)
            return jsonify(value) 
    else:
        error = Error("specify arg month", 400)
        return jsonify(error.reason), error.code
