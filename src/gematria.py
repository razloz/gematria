"""
Gematria Lib
"""
import json
from os import path
#LATIN = str([chr(i) for i in range(ord('\u0000'), ord('\u007F'))])
LATIN_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LATIN_LOWER = 'abcdefghijklmnopqrstuvwxyz'
LATIN_FULL = '0123456789' + LATIN_UPPER + LATIN_LOWER
#GREEK = str([chr(i) for i in range(ord('\u0370'), ord('\u03FF'))])
GREEK_UPPER = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
GREEK_LOWER = 'αβγδεζηθικλμνξοπρσςτυφχψω'
GREEK_FULL = GREEK_UPPER + GREEK_LOWER
#HEBREW = str([chr(i) for i in range(ord('\u0590'), ord('\u05FF'))])
UNICODE = str([chr(i) for i in range(256)])
SRC_PATH = path.dirname(path.realpath(__file__))
LEXICON_PATH = path.abspath(f'{SRC_PATH}/resources/lexicon.json')
HIDDEN_PATH = path.abspath(f'{SRC_PATH}/resources/hidden.json')
FAVORITE_PATH = path.abspath(f'{SRC_PATH}/resources/favorite.json')
WORDS_PATH = path.abspath(f'{SRC_PATH}/resources/words.txt')


def fibonacci(n=26):
    """
    Generator for the Fibonacci sequence up to the nth iteration.
    """
    steps_taken = 0
    previous_number = 0
    current_number = 1
    while steps_taken <= n:
        next_number = previous_number + current_number
        previous_number = current_number
        current_number = next_number
        steps_taken += 1
        yield next_number


def numerology(number, reduce_to=1):
    """
    Reduce number to a set length.
    """
    x = str(number)
    while len(x) > reduce_to:
        x = str(sum([int(n) for n in x]))
    return int(x)


def gematria(word, alphabet=LATIN_UPPER, reverse=False, full_reduce=False, count_type=1):
    """
    Pair letters with numbers.
    """
    if alphabet == LATIN_UPPER:
        alphabet = str(alphabet).upper()
        word = str(word).upper()
    if reverse:
        alphabet = alphabet[::-1]
    gem = dict()
    i = 1
    incr = 1
    fib = [i for i in fibonacci(n=len(alphabet))] if count_type == 4 else []
    for letter in alphabet:
        if count_type == 1:
            gem[letter] = i
            i += 1
        elif count_type == 2:
            gem[letter] = i * 6
            i += 1
        elif count_type == 3:
            gem[letter] = i
            i += incr
            if i == 10 or i == 100 or i == 1000:
                incr *= 10
        elif count_type == 4:
            gem[letter] = fib[i - 1]
            i += 1
    if full_reduce:
        n = numerology(sum([i for i in gem.values()]))
        i = 1
        reduced = dict()
        for letter in alphabet:
            reduced[letter] = i
            i += 1
            if i > n: i = 1
        return sum([reduced[l] if l in alphabet else 0 for l in word])
    else:
        return sum([gem[l] if l in alphabet else 0 for l in word])


def full_test(word):
    """
    Gets every number for given word or statement.
    """
    standard = gematria(word, reverse=False, full_reduce=False, count_type=1)
    reverse_standard = gematria(word, reverse=True, full_reduce=False, count_type=1)
    reduction = gematria(word, reverse=False, full_reduce=True, count_type=1)
    reverse_reduction = gematria(word, reverse=True, full_reduce=True, count_type=1)
    sumerian = gematria(word, reverse=False, full_reduce=False, count_type=2)
    reverse_sumerian = gematria(word, reverse=True, full_reduce=False, count_type=2)
    jewish = gematria(word, reverse=False, full_reduce=False, count_type=3)
    reverse_jewish = gematria(word, reverse=True, full_reduce=False, count_type=3)
    fib_reduced = gematria(word, reverse=False, full_reduce=True, count_type=4)
    reverse_fib_reduced = gematria(word, reverse=True, full_reduce=True, count_type=4)
    test_results = [
        standard, reverse_standard,
        reduction, reverse_reduction,
        sumerian, reverse_sumerian,
        jewish, reverse_jewish,
        fib_reduced, reverse_fib_reduced
    ]
    return test_results


def save_json(real_path, data):
    """
    Take dict like data and store it as a json object.
    """
    try:
        with open(real_path, 'w') as wf:
            wf.write(json.dumps(data))
    except:
        print(f"*** Failed to save data to {real_path} ***")


def load_json(real_path):
    """
    Get dict like data from a json object.
    """
    try:
        with open(real_path, 'r') as rf:
            data = dict(json.load(rf))
        return data
    except:
        print(f"*** Failed to load data from {real_path} ***")
        return None


def get_hidden():
    """
    Helper function for loading the hidden words.
    """
    return load_json(HIDDEN_PATH)


def get_favorite():
    """
    Helper function for loading the favorite words.
    """
    return load_json(FAVORITE_PATH)


def get_lexicon():
    """
    Helper function for loading the lexicon.
    """
    return load_json(LEXICON_PATH)


def save_hidden(data):
    """
    Helper function for saving the hidden words.
    """
    save_json(HIDDEN_PATH, data)


def save_favorite(data):
    """
    Helper function for saving the hidden words.
    """
    save_json(FAVORITE_PATH, data)


def save_lexicon(data):
    """
    Helper function for saving the hidden words.
    """
    save_json(LEXICON_PATH, data)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('word', type=str, nargs='*', default='Gematria',
                   help='Word or statement to check against alphabet.')
    args = p.parse_args()
    word = ''
    for w in args.word: word += str(w).upper() + ' '
    if word[-2:-1] == ' ': word = word[:-2]
    test_results = full_test(word)
    print(f'{word}: {test_results}')
    if not path.exists(HIDDEN_PATH):
        save_hidden(dict())
    if not path.exists(FAVORITE_PATH):
        save_favorite(dict())
    if not path.exists(LEXICON_PATH):
        l = list()
        with open(WORDS_PATH, 'r') as rf:
            raw_words = rf.readlines()
        for rw in raw_words:
            r = str(rw).replace("""\n""", "").upper()
            for w in r.split():
                for c in list(w):
                    if c not in LATIN_UPPER:
                        w = str(w).replace(c, "")
                if w not in l:
                    if len(w) > 0:
                        l.append(w)
        u = set(l)
        lexicon = dict()
        for r in u:
            lexicon[r] = full_test(r)
        save_lexicon(lexicon)
