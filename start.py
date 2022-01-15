#!./venv/bin/python

# Script parses messages exported from a Telegram chat as json
# to find locations where people gather to play volleyball

import json

from googletrans import Translator
import pymorphy2


TELEGRAM_CHAT_EXPORT_RESULT_FILE_PATH = '/home/edvein-rin/\
Downloads/ChatExport_2022-01-15/result.json'

translator = Translator()
morph = pymorphy2.MorphAnalyzer()


def translate(text):
    return translator.translate(text).text


def morph_word(word, gramema='loct'):
    parsed_word = morph.parse(word)[0]
    if (parsed_word):
        inflected_word = parsed_word.inflect({gramema})
        if (inflected_word):
            return inflected_word.word

    return word


def is_word_in_text(text, word):
    def conditions(word):
        return any([
            text.startswith(word + ' '),
            text.endswith(' ' + word),
            text.find(' ' + word + ' ') != -1,
        ])

    word_cases = [word.lower(), word, word.capitalize()]

    for word_in_case in word_cases:
        word_morphs = set([word_in_case, morph_word(word_in_case)])
        for word_morph in word_morphs:
            if conditions(word_morph):
                return word_morph

    return False


def has_message_underground_mentions(message):
    underground_names = ['м.', 'метро']
    metro_stations = [
        'Академгородок', 'Академмістечко', 'Житомирская', 'Житомирська', 'Святошин', 'Святошин', 'Нивки', 'Нивки', 'Берестейская', 'Берестейська', 'Шулявская', 'Шулявська', 'Политехнический институт', 'Політехнічний інститут', 'Вокзальная', 'Вокзальна', 'Университет', 'Університет', 'Театральная', 'Театральна', 'Крещатик', 'Хрещатик', 'Арсенальная', 'Арсенальна', 'Днепр', 'Дніпро', 'Гидропарк', 'Гідропарк', 'Левобережная', 'Лівобережна', 'Дарница', 'Дарниця', 'Черниговская', 'Чернігівська', 'Лесная', 'Лісова', 'Героев Днепра', 'Героїв Дніпра', 'Минская', 'Мінська', 'Оболонь', 'Оболонь', 'Почайна', 'Почайна', 'Тараса Шевченко', 'Тараса Шевченка', 'Контрактовая площадь', 'Контрактова площа', 'Почтовая площадь', 'Поштова площа', 'Площадь Независимости', 'Майдан Незалежності', 'Площадь Льва Толстого', 'Площа Льва Толстого', 'Олимпийская', 'Олімпійська', 'Дворец Украина', 'Палац «Україна»', 'Лыбедская', 'Либідська', 'Демиевская', 'Деміївська', 'Голосеевская', 'Голосіївська', 'Васильковская', 'Васильківська', 'Выставочный центр', 'Виставковий центр', 'Ипподром', 'Іподром', 'Теремки', 'Теремки', 'Сырец', 'Сирець', 'Дорогожичи', 'Дорогожичі', 'Лукьяновская', "Лук'янівська", 'Золотые ворота', 'Золоті ворота', 'Дворец спорта', 'Палац спорту', 'Кловская', 'Кловська', 'Печерская', 'Печерська', 'Дружбы народов', 'Дружби народів', 'Выдубичи', 'Видубичі', 'Славутич', 'Славутич', 'Осокорки', 'Осокорки', 'Позняки', 'Позняки', 'Харьковская', 'Харківська', 'Вырлица', 'Вирлиця', 'Бориспольская', 'Бориспільська', 'Красный хутор', 'Червоний хутір'
    ]
    casual_metro_stations = [
        'Академ', 'Шулявка', 'Политех', 'Політех', 'Вокзал', 'Универ', 'Універ', 'Героев', 'Героїв', 'Контрактовая', 'Контрактова', 'Почтовая', 'Почтова', 'Голосеево', 'Голосіїва', 'Иподром', 'Левобережна', 'Житомирска', 'Житомирська', 'Берестейска', 'Голосеевска', 'Васильковска', 'Лукьяновска', 'Кловска', 'Печерска', 'Харьковска', 'Бориспольска', 'Демієвська',
    ]
    words_to_search = metro_stations + casual_metro_stations + underground_names
    for word in words_to_search:
        word_in_text = is_word_in_text(message, word)
        if (word_in_text):
            print(word_in_text, message)
            return True

    return False


def analyze_messages(messages):
    underground_mentions = []
    for message in messages:
        if has_message_underground_mentions(message):
            underground_mentions.append(message)

    number_of_underground_mentions = len(underground_mentions)
    print(f'Number of messages \
with underground mentions: {number_of_underground_mentions}')

    # test_message = underground_mentions[0]
    # translated_test_message = translate(test_message)
    # print(test_message)
    # print(translated_test_message)


def main():
    with open(TELEGRAM_CHAT_EXPORT_RESULT_FILE_PATH) as file:
        messages = json.loads(file.read())['messages']

        text_messages = []
        for message in messages[:600]:
            text = message['text']
            if message['type'] == 'message':
                if isinstance(text, str):
                    if text != '':
                        text_messages.append(text)
                elif isinstance(text, list):
                    text_messages.append(
                        ''.join([text_part if isinstance(text_part, str) else '' for text_part in text]))
                else:
                    raise('error')

        number_of_text_messages = len(text_messages)
        print(f'Overall number of text messages: {number_of_text_messages}')

        analyze_messages(text_messages)


if __name__ == '__main__':
    main()

# Metro stations were parsed via browser parser and this shit below
# sum([[metro.split('(')[0], metro.split('(')[1][5:-1]]
#      for metro in metro_stations.split('\n')[1:-1]], [])
