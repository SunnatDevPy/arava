# import requests
# from bs4 import BeautifulSoup
#
#
# def fetch_exchange_rates(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         value_element = soup.select_one('.other-bank-course-block-bottom .cours-active .semibold-text')
#         if value_element:
#             value = value_element.get_text(strip=True)
#             print(value)  # Output: 12 805 so'm
#     except Exception as e:
#         print(f"Error parsing the data: {e}")
#
#         soup.select_one(
#             'body > div.page-container > div.page-container__body > div:nth-child(7) > div > div.inform-page > div.left-side > div.other-bank-course-block.row > div.other-bank-course-block-bottom.row > div.col-2.cours-active > span.semibold-text')
#
#
# url = 'https://bank.uz/uz/'
# fetch_exchange_rates(url)

import random

# Призы и их вероятности (в процентах)
prizes = [
    {"name": "Меч", "chance": 40},  # 40% шанс
    {"name": "Щит", "chance": 25},  # 25% шанс
    {"name": "Кольцо", "chance": 20},  # 20% шанс
    {"name": "Зелье здоровья", "chance": 10},  # 10% шанс
    {"name": "Редкий артефакт", "chance": 5},  # 5% шанс
]

def open_chest():
    # Создаем список диапазонов для вероятностей
    ranges = []
    current_range = 0
    for prize in prizes:
        ranges.append((current_range, current_range + prize["chance"], prize["name"]))
        current_range += prize["chance"]

    # Генерируем случайное число от 0 до 100
    random_number = random.uniform(0, 100)

    # Находим, в какой диапазон попало число
    for start, end, name in ranges:
        if start <= random_number < end:
            return name

# Открытие сундука
if __name__ == "__main__":
    print("Вы открыли сундук!")
    reward = open_chest()
    print(f"Ваш приз: {reward}")