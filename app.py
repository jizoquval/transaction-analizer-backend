from model.cashback import Cashback
from model.error import Error
from flask import Flask, jsonify
from flask import request
from controller import user as user_controller

app = Flask(__name__)

cashbacks = {'Финансовые услуги': 5, 'Одежда/Обувь': 5, 'Разные товары': 5, 'Супермаркеты': 5, 'Красота': 5, 'Сувениры': 5, 'Фаст Фуд': 5, 'Дом/Ремонт': 5, 'Сервисные услуги': 5, 'Транспорт': 5, 'Медицинские услуги': 5, 'Топливо': 5, 'Наличные': 5, 'Связь/Телеком': 5, 'Частные услуги': 5, 'Рестораны': 5,
             'Развлечения': 5, 'НКО': 5, 'Книги': 5, 'Кино': 5, 'Автоуслуги': 5, 'Музыка': 5, 'Отели': 5, 'Аптеки': 5, 'Цветы': 5, 'Ж/д билеты': 5, 'Авиабилеты': 5, 'Спорттовары': 5, 'Госсборы': 5, 'Аренда авто': 5, 'Животные': 5, 'Duty Free': 5, 'Турагентства': 5, 'Образование': 5, 'Искусство': 5, 'Фото/Видео': 5}


@app.route('/')
def index():
    return "<h1>Welcome!</h1>"


@app.route("/user/list")
def get_users():
    return user_controller.get_list()


@app.route("/user/result/<string:user_id>")
def get_result_for(user_id):
    return user_controller.get_result_by(user_id)


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
    if month:
        return f'get metrics for all users by months {month}'
    else:
        return "get metrics for all users"
