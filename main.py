from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://pyatsentyuk:tiger66one@cluster0.epc74.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.test
collection = db.cats


# Читання (Read)
# Функція для виведення всіх записів із колекції.
def read_all_cats():
    print('test');
    cats = collection.find()
    for cat in cats:
        print(cat)


# Функція, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
def find_cat_by_name():
    name = input("Введіть ім'я кота: ")
    cat = collection.find_one({"name": name})
    if cat:
        print(f"Знайдено кота: {cat}")
    else:
        print("Кота з таким ім'ям не знайдено.")


# Оновлення (Update)
# Функція, яка дозволяє користувачеві оновити вік кота за ім'ям.
def update_cat_age_by_name():
    name = input("Введіть ім'я кота для оновлення віку: ")
    new_age = int(input("Введіть новий вік кота: "))

    result = collection.update_one(
        {"name": name},
        {"$set": {"age": new_age}}
    )

    # Перевіряємо, чи було оновлено документ
    if result.matched_count > 0:
        print(f"Вік кота з ім'ям '{name}' успішно оновлено до {new_age}.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")


# Функція, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
def add_feature_to_cat_by_name():
    name = input("Введіть ім'я кота: ")
    new_feature = input("Введіть нову характеристику кота: ")

    result = collection.update_one(
        {"name": name},
        {"$push": {"features": new_feature}}
    )

    # Перевіряємо, чи було оновлено документ
    if result.matched_count > 0:
        print(f"Нову характеристику '{new_feature}' успішно додано коту з ім'ям '{name}'.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")


# Функція для видалення запису з колекції за ім'ям тварини.
def delete_cat_by_name():
    name = input("Введіть ім'я кота для видалення: ")

    result = collection.delete_one({"name": name})

    if result.deleted_count > 0:
        print(f"Кота з ім'ям '{name}' успішно видалено.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")


# функція для видалення всіх записів із колекції.
def delete_all_cats():
    confirmation = input("Ви впевнені, що хочете видалити всі записи? (так/ні): ")

    if confirmation.lower() == "так":
        result = collection.delete_many({})
        print(f"Успішно видалено {result.deleted_count} записів.")
    else:
        print("Операцію скасовано.")
