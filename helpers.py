import re
import string


def remove_punctuations(text):
    return re.sub(r"[,.;@#?!&$]+\ *", " ", text)


def is_sub_in_text(sub, text):
    text = remove_punctuations(text)

    def conditions(sub):
        return any([
            text.startswith(sub + ' '),
            text.endswith(' ' + sub),
            text.find(' ' + sub) != -1,
        ])

    sub_cases = [sub.lower(), sub, sub.capitalize(), string.capwords(sub)]

    for sub_in_case in sub_cases:
        if conditions(sub_in_case):
            return True

    return False
