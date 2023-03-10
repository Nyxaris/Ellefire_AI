# Автор: Nyxaris
# Дата обновления: 10.03.23 

import json
import random
import requests

# Ссылка на словарный запас из файла word.json
url = 'https://raw.githubusercontent.com/Nyxaris/Ellefire_AI/main/words.json'

# Загрузка данных "words.json"
try:
    response = requests.get(url)
    response.raise_for_status()
    data = json.loads(response.text)
except requests.exceptions.RequestException as e:
    print("Не удалось загрузить данные:", e)
    data = []

# Сохранение данных в файл "words.json"
def save_data(data):
    with open("words.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Ввод вопроса и вывод ответа
while True:
    user_input = input("Вы: ")
    if user_input.strip() == "":
        continue
    response = None
    # Поиск подходящего ответа в базе данных
    matching_items = [item for item in data if item["message"].lower() in user_input.lower()]
    if matching_items:
        # Если заданный вопрос есть в базе данных то даём на него ответ
        response = random.choice(matching_items)["response"]
    else:
        # Если заданного вопроса нет в базе данных то бот даст рандомный ответ
        response = random.choice(data)["response"]
    # Выбираем один из ответов на поставленный вопрос
    if isinstance(response, list):
        response = random.choice(response)
    print("Nyx:", response)
