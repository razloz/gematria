ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
UNICODE = str([chr(i) for i in range(256)])

def numerology(number):
	"""Reduce integer to a single digit."""
	x = str(number)
	while len(x) > 1:
		x = str(sum([int(n) for n in x]))
	return int(x)

def gematria(word, alphabet=ALPHABET, reverse=False, full_reduce=False):
	"""Pair letters with numbers."""
	if alphabet == ALPHABET:
		alphabet = str(ALPHABET).upper()
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
		return sum([reduced[letter] for letter in word])
	else:
		return sum([gem[letter] for letter in word])

def test_all():
	word = 'gematria'
	print('Word: gematria')
	ka = {"alphabet": UNICODE, "reverse": False, "full_reduce": False}
	print(f'Standard: {gematria(word, **ka)}')
	ka['reverse'] = True
	print(f'Reverse Standard: {gematria(word, **ka)}')
	ka['reverse'] = False
	ka['full_reduce'] = True
	print(f'Full Reduction: {gematria(word, **ka)}')
	ka['reverse'] = True
	print(f'Reverse Full Reduction: {gematria(word, **ka)}')
