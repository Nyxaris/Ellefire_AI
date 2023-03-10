# Автор: Nyxaris
# Дата обновления: 10.03.23 

import json
import random
import requests

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

# Загрузка словарного запаса из файла word.json
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

# Обработка запроса пользователя
def process_input(user_input):
    # Загрузка стоп-слов
    stop_words = set(stopwords.words('english'))

    # Токенизация запроса пользователя
    tokens = word_tokenize(user_input)

    # Удаление стоп-слов из запроса пользователя
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Обработка запроса с помощью обработчиков
    matching_responses = []
    for item in data:
        for keyword in item.get('keywords', []):
            if keyword.lower() in filtered_tokens:
                matching_responses.append(item['response'])

    # Возвращаем случайный ответ, если не найдено подходящего обработчика
    if not matching_responses:
        return random.choice(data)['response']

    # Возвращаем случайный подходящий ответ
    return random.choice(matching_responses)

# Поиск информации в Интернете
def search(query):
    try:
        # Выполнение GET-запроса к поисковому движку
        response = requests.get('https://www.google.com/search?q=' + query)

        # Проверка успешности запроса
        if response.status_code == 200:
            # Извлечение результата поиска
            result = response.text
            return result
        else:
            print("Ошибка:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Не удалось выполнить запрос:", e)
        return None

# Ввод запроса и вывод ответа
while True:
    user_input = input("Вы: ")
    if user_input.strip() == "":
        continue
    response = None

    # Обработка запроса пользователя
    response = process_input(user_input)

    # Если не найдено подходящего ответа, выполняем поиск в Интернете
    if not response:
        result = search(user_input)
        if result:
            print(result)
        else:
            print("Извините, не удалось найти ответ на ваш запрос.")
    else:
        # Вывод ответа
        if isinstance(response, list):
            print("Nyx:", random.choice(response))
        else:
            print("Nyx:", response)
