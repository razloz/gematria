"""
Gematria Lib
"""
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ALPHANUM = 'abcdefghijklmnopqrstuvwxyz0123456789'
GREEK_UPPER = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
GREEK_LOWER = 'αβγδεζηθικλμνξοπρσςτυφχψω'
GREEK_FULL = GREEK_UPPER + GREEK_LOWER
#HEBREW = str([chr(i) for i in range(ord('\u0590'), ord('\u05FF'))])
UNICODE = str([chr(i) for i in range(256)])


def numerology(number, reduce_to=1):
    """Reduce number to a set length."""
    x = str(number)
    while len(x) > reduce_to:
        x = str(sum([int(n) for n in x]))
    return int(x)


def gematria(word, alphabet=ALPHABET, reverse=False, full_reduce=False):
    """Pair letters with numbers."""
    if alphabet == ALPHABET or ALPHANUM:
        alphabet = str(alphabet).upper()
        word = str(word).upper()
    if reverse:
        alphabet = alphabet[::-1]
    gem = dict()
    i = 1
    for letter in alphabet:
        gem[letter] = i
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


def full_test(word, alphabet):
    """Returns the standard, reduced, and their reverses."""
    ka = {"reverse": False, "full_reduce": False}
    if alphabet == 1:
        ka['alphabet'] = ALPHABET
    elif alphabet == 2:
        ka['alphabet'] = ALPHANUM
    else:
        ka['alphabet'] = UNICODE
    standard = gematria(word, **ka)
    ka['reverse'] = True
    reverse_standard = gematria(word, **ka)
    ka['reverse'] = False
    ka['full_reduce'] = True
    full_reduction = gematria(word, **ka)
    ka['reverse'] = True
    reverse_full_reduction = gematria(word, **ka)
    return [standard, reverse_standard, full_reduction, reverse_full_reduction]


def get_lexicon(alphabet):
    import json
    from os import path
    SRC_PATH = path.dirname(path.realpath(__file__))
    JSON_PATH = path.abspath(f'{SRC_PATH}/resources/gematria.json')
    WORDS_PATH = path.abspath(f'{SRC_PATH}/words.txt')
    lexicon = dict()
    if not path.exists(JSON_PATH):
        with open(WORDS_PATH, 'r') as rf:
            raw_words = rf.readlines()
        for rw in raw_words:
            r = str(rw).replace("""\n""", "").upper()
            lexicon[r] = full_test(r, alphabet)
        with open(JSON_PATH, 'w') as wf:
            wf.write(json.dumps(lexicon))
        print('*** Finished creating gematria.json ***')
    else:
        with open(JSON_PATH, 'r') as rf:
            lexicon = dict(json.load(rf))
        print('*** Lexicon loaded from gematria.json ***')
    return lexicon


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('word', type=str, nargs='*', default='Gematria',
                   help='Word or statement to check against alphabet.')
    p.add_argument('--alphabet', type=int, nargs=1, default=1,
                   help='1=ALPHABET, 2=ALPHANUM, 3=UNICODE.')
    p.add_argument('--matches', type=int, nargs=1, default=4,
                   help='Number of matches to display.')
    args = p.parse_args()
    matches = int(args.matches[0])
    word = ''
    for w in args.word: word += str(w).upper() + ' '
    if word[-2:-1] == ' ': word = word[:-2]
    test_results = full_test(word, args.alphabet)
    print(f'{word}: {test_results}')

    lexicon = get_lexicon(args.alphabet)
    for l, r in lexicon.items():
        c = 0
        if test_results[0] == r[0]: c += 1
        if test_results[1] == r[1]: c += 1
        if test_results[2] == r[2]: c += 1
        if test_results[3] == r[3]: c += 1
        if c == matches:
            print(f'{l}: {r}')

    for w in word.split():
        try:
            search_results = lexicon[str(w)]
            print(f'{w}: {search_results}')
            for l, r in lexicon.items():
                c = 0
                if search_results[0] == r[0]: c += 1
                if search_results[1] == r[1]: c += 1
                if search_results[2] == r[2]: c += 1
                if search_results[3] == r[3]: c += 1
                if c == matches:
                    print(f'{l}: {r}')
        except:
            print(f'{w}: not in lexicon.')
