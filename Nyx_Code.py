# Автор : Nyxaris
# Дата обновления : 10.03.2023

import json
import random
import requests
import time

# Ссылка на файл word.json в репозитории Github
url = 'https://raw.githubusercontent.com/Nyxaris/Ellefire_AI/main/words.json'

# Проверка доступности интернет-соединения
while True:
    try:
        requests.get("http://www.google.com", timeout=1)
        # print("Интернет-соединение установлено")
        break
    except requests.exceptions.RequestException:
        print("Интернет-соединение недоступно, ожидаем 10 секунд...")
        time.sleep(10)

# Загрузка данных из файла "words.json"
try:
    response = requests.get(url)
    response.raise_for_status()
    data = json.loads(response.text)
    if not isinstance(data, list):
        raise ValueError("Некорректный формат данных в файле words.json")
    for item in data:
        if "message" not in item or "response" not in item:
            raise ValueError("Некорректный формат данных в файле words.json")
except (requests.exceptions.RequestException, ValueError) as e:
    print("Не удалось загрузить данные:", e)
    data = []

# Функция для сохранения данных в файл "words.json"
def save_data(data):
    with open("words.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Обработка ввода пользователя и вывод ответа от компьютера
while True:
    user_input = input("Вы: ")
    if user_input.strip() == "":
        continue
    response = None
    # Поиск подходящего ответа в базе данных
    matching_items = [item for item in data if item["message"].lower() in user_input.lower()]
    if matching_items:
        # Если есть подходящие ответы, то выбираем случайный из них
        response = random.choice(matching_items)["response"]
    else:
        # Если подходящего ответа нет, то даем рандомный ответ из базы данных
        response = random.choice(data)["response"]
    # Если ответ - список, выбираем из него случайный элемент
    if isinstance(response, list):
        response = random.choice(response)
    print("Nyx:", response)
