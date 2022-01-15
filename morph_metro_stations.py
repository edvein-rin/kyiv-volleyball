import json

import pymorphy2

from constants import METRO_STATIONS_FILE, METRO_STATIONS_MORPHED_FILE

HAND_FIXES = {
    'Дарница': ['Дарницы'],
    'Берестейская': ['Берестейки']
}


morph_ru = pymorphy2.MorphAnalyzer(lang='ru')
morph_uk = pymorphy2.MorphAnalyzer(lang='uk')


def morph_word(word, lang='ru', gramema='loct'):
    parsed_word = (morph_ru if lang == 'ru' else morph_uk).parse(word)[0]
    if (parsed_word):
        inflected_word = parsed_word.inflect({gramema})
        if (inflected_word):
            return inflected_word.word

    return word


def morph_text(text, lang='ru', gramema='loct'):
    words = text.split()
    new_words = []
    for word in words:
        new_words.append(morph_word(word, lang))
    return ' '.join(new_words)


def main():
    with open(METRO_STATIONS_FILE, 'r') as input_file:
        metro_stations = json.load(input_file)
        morphed_metro_stations = {}

        for metro_station_key, metro_station in metro_stations.items():
            metro_station_names = []
            metro_station_ru_names = metro_station['ru']
            metro_station_uk_names = metro_station['uk']

            for name in metro_station_ru_names:
                # Именительный: Метро Левобережная
                metro_station_names.append(name)
                # Предложный: На Минской
                metro_station_names.append(morph_text(name, 'ru', 'loct'))
                # Родительный: Район Университета
                metro_station_names.append(morph_text(name, 'ru', 'gent'))

            for name in metro_station_uk_names:
                metro_station_names.append(name)
                metro_station_names.append(morph_text(name, 'uk', 'loct'))
                metro_station_names.append(morph_text(name, 'uk', 'gent'))

            if metro_station_key in HAND_FIXES:
                metro_station_names.append(*HAND_FIXES[metro_station_key])

            morphed_metro_stations[metro_station_key] = list(
                set(metro_station_names))

        with open(METRO_STATIONS_MORPHED_FILE, 'w') as output_file:
            json.dump(morphed_metro_stations, output_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
