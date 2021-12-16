"""
Gematria Lib
"""
#LATIN = str([chr(i) for i in range(ord('\u0000'), ord('\u007F'))])
#GREEK = str([chr(i) for i in range(ord('\u0370'), ord('\u03FF'))])
#HEBREW = str([chr(i) for i in range(ord('\u0590'), ord('\u05FF'))])
#UNICODE = str([chr(i) for i in range(256)])
EN_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
EN_LOWER = 'abcdefghijklmnopqrstuvwxyz'
EN_FULL = EN_UPPER + EN_LOWER
EN_NUMERIC = EN_FULL + '0123456789'


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


def gematria(word, alphabet=EN_UPPER, reverse=False, full_reduce=False, case=1):
    """
    Pair letters with numbers.
    """
    if alphabet == EN_UPPER:
        word = str(word).upper()
    if reverse:
        alphabet = alphabet[::-1]
    gem = dict()
    i = 1
    incr = 1
    f = len(alphabet)
    nth = int(f * 0.5)
    nth = nth + 1 if nth * 2 < f else nth
    fib = [i for i in fibonacci(n=nth)] if case == 4 else []
    fib = fib + fib if len(fib) > 0 else fib
    for letter in alphabet:
        if case == 1:
            gem[letter] = i
            i += 1
        elif case == 2:
            gem[letter] = i * 6
            i += 1
        elif case == 3:
            gem[letter] = i
            i += incr
            if i == 10 or i == 100 or i == 1000:
                incr *= 10
        elif case == 4:
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
    standard = gematria(word)
    rev_standard = gematria(word, reverse=True)
    reduction = gematria(word, full_reduce=True)
    rev_reduction = gematria(word, reverse=True, full_reduce=True)
    sumerian = gematria(word, case=2)
    rev_sumerian = gematria(word, reverse=True, case=2)
    jewish = gematria(word, case=3)
    rev_jewish = gematria(word, reverse=True, case=3)
    fib = gematria(word, case=4)
    rev_fib = gematria(word, reverse=True, case=4)
    test_results = [
        standard, rev_standard,
        reduction, rev_reduction,
        sumerian, rev_sumerian,
        jewish, rev_jewish,
        fib, rev_fib
    ]
    return test_results


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
