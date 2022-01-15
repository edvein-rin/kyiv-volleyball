#!./venv/bin/python

# Script parses messages exported from a Telegram chat as json
# to find locations where people gather to play volleyball

import json

from constants import METRO_STATIONS_MORPHED_FILE
from helpers import is_sub_in_text


TELEGRAM_CHAT_EXPORT_RESULT_FILE_PATH = '/home/edvein-rin/\
Downloads/ChatExport_2022-01-15/result.json'
SHOW_WARNINGS = False


def find_metro_mentions_in_message(message, metro_stations):
    metro_mentions = []
    for metro_station_key, metro_station_names in metro_stations.items():
        for metro_station_name in metro_station_names:
            if (is_sub_in_text(metro_station_name, message)):
                metro_mentions.append(metro_station_key)

    if (metro_mentions):
        return metro_mentions

    if (SHOW_WARNINGS):
        metro_prefixes = ['м.', 'метро', 'станция',
                          'станцию', 'станции', 'станцие']
        for prefix in metro_prefixes:
            if (is_sub_in_text(prefix, message)):
                print(
                    'WARNING Metro name possibly was\'nt ' +
                    f'recognized in the message below:\n{message}\n')

    return []


def analyze_metro_mentions(messages):
    with open(METRO_STATIONS_MORPHED_FILE, 'r') as f:
        morphed_metro_stations = json.load(f)

        metro_mentions = {}
        number_of_metro_mentions = 0

        for message in messages:
            metro_mentions_in_message = find_metro_mentions_in_message(
                message, morphed_metro_stations)
            if (len(metro_mentions_in_message) != 0):
                number_of_metro_mentions += 1

            for mentioned_metro in metro_mentions_in_message:
                if (mentioned_metro not in metro_mentions):
                    metro_mentions[mentioned_metro] = []
                metro_mentions[mentioned_metro].append(message)

        print('Количество сообщений где упоминали названия метро: ' +
              str(number_of_metro_mentions))

        messages_per_metro = {}
        for metro_name, messages in metro_mentions.items():
            messages_per_metro[metro_name] = len(messages)

        print('Станции метро отсортированные по количеству упоминаний:')
        for metro in sorted(messages_per_metro,
                            key=messages_per_metro.get,
                            reverse=True):
            number_of_messages = messages_per_metro[metro]
            print(f'{metro}: {number_of_messages}')


def analyze_streets_mentions(messages):
    street_prefixes = [
        'вул.', 'вулиця', 'вулиці',
        'ул.', 'улица', 'улицы', 'улице',
        'адрес', 'адресу', 'адреса', 'адресс',
        'адресі',
        'проспект', 'проспекту', 'проспекте',
        'проспекті',
        'бульвар', 'бульваре', 'бульвару',
        'бульварі',
        'переулок', 'переулку',
    ]
    number_of_messages_with_streets = 0
    for message in messages:
        for street_prefix in street_prefixes:
            if is_sub_in_text(street_prefix, message):
                number_of_messages_with_streets += 1
    print('Количество сообщений где упоминали ' +
          f'названия улиц: {number_of_messages_with_streets}')


def analyze_messages(messages):
    analyze_metro_mentions(messages)
    analyze_streets_mentions(messages)


def main():
    with open(TELEGRAM_CHAT_EXPORT_RESULT_FILE_PATH, 'r') as f:
        messages = json.load(f)['messages']

        text_messages = []
        for message in messages:
            text = message['text']
            if message['type'] == 'message':
                if isinstance(text, str):
                    if text != '':
                        text_messages.append(text)
                elif isinstance(text, list):
                    text_message = ''.join([text_part if isinstance(
                        text_part, str) else '' for text_part in text])
                    text_messages.append(text_message)
                else:
                    raise('error')

        number_of_text_messages = len(text_messages)
        print('Количество сообщений в чате: ' +
              str(number_of_text_messages))

        analyze_messages(text_messages)


if __name__ == '__main__':
    main()
