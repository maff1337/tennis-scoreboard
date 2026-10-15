import unicodedata


def has_single_alphabet(value: str) -> bool:
    alphabets: set[str] = set()

    for char in value:
        if not char.isalpha():
            continue

        char_name = unicodedata.name(char, '')

        if 'LATIN' in char_name:
            alphabets.add('latin')
        elif 'CYRILLIC' in char_name:
            alphabets.add('cyrillic')
        else:
            return False

    return len(alphabets) == 1
