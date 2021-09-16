from model.user import User
from model.database import Session
from model.cashback_category import Category
import csv
from multiprocessing.dummy import Pool as ThreadPool


def set_inital_data():
    session = Session()
    categories = ['Финансовые услуги', 'Наличные', 'Разные товары', 'Транспорт',
                  'Супермаркеты', 'Фаст Фуд', 'Топливо', 'Связь/Телеком',
                  'Дом/Ремонт', 'Животные', 'Рестораны', 'Сувениры', 'Аренда авто',
                  'Медицинские услуги', 'Турагентства', 'Спорттовары', 'Аптеки',
                  'Цветы', 'Госсборы', 'Одежда/Обувь', 'Книги', 'Музыка', 'Красота',
                  'Сервисные услуги', 'Кино', 'Авиабилеты', 'Частные услуги',
                  'Развлечения', 'НКО', 'Автоуслуги', 'Отели', 'Ж/д билеты',
                  'Образование', 'Искусство', 'Фото/Видео', 'Duty Free']

    for cat in categories:
        session.add(Category(name=cat, cashback=0.05))
    session.commit()

    with open('res/unique_party_rk.csv', newline='') as users:
        reader = csv.DictReader(users, fieldnames=["party_rk"])
        pool = ThreadPool(4)
        users_ids = list(pool.map(lambda x: x["party_rk"], reader))
        pool.close()
        users_ids.pop(0)
        for id in users_ids:
             session.add(User(party_rk=id))
        session.commit()
    session.close()