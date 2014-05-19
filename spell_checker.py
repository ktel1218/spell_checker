# Write a program that reads a large list of English words (e.g. from /usr/share/dict/words on a unix system) into memory, and then reads words from stdin, and prints either the best spelling suggestion, or "NO SUGGESTION" if no suggestion can be found. The program should print "> " as a prompt before reading each word, and should loop until killed.

# Your solution should be faster than O(n) per word checked, where n is the length of the dictionary. That is to say, you can't scan the dictionary every time you want to spellcheck a word.

# For example:
#  > sheeeeep
#  sheep
#  > peepple
#  people
#  > sheeple
#  NO SUGGESTION

# The class of spelling mistakes to be corrected is as follows:

# Case (upper/lower) errors:
#  "inSIDE" => "inside"

# Repeated letters:
#  "jjoobbb" => "job"

# Incorrect vowels:
#  "weke" => "wake"

# In addition, any combination of the above types of error in a single word should be corrected (e.g. "CUNsperrICY" => "conspiracy").

# If there are many possible corrections of an input word, your program can choose one in any way you like, however your results *must* match the examples above (e.g. "sheeeeep" should return "sheep" and not "shap").

# Final step: Write a second program that generates words with spelling mistakes of the above form, starting with correctly spelled English words. Pipe its output into the first program and verify that there are no occurrences of "NO SUGGESTION" in the output.

# Submit your test here:
# http://boards.greenhouse.io/tests/4f6b4d24110c84b562c0cd84aa402614


import itertools

from sys import argv

test_words = []
if len(argv) == 2:
	test_words = list(open(argv[1], 'r'))

def make_dictionary():
	''' make our dictionary '''

	dictionary = {}

	words = open('words.txt', 'r') # from /usr/share/dict/words

	for line in words:
		dictionary[line.strip()] = 0
	words.close()

	frequency = open('word_frequency.txt', 'r') # from http://jbauman.com/gsl.html

	for line in frequency:
		line = line.split()
		key = line[2]
		value = line[1]
		dictionary.setdefault(key, 0)
		dictionary[key] += int(value)
	frequency.close()

	return dictionary


def uniquify_letters(word):
	''' whittle down repeat blocks of letters to 1 '''
	word = list(word)
	for index, letter in enumerate(word):
		while index+1 < len(word) and letter == word[index+1]:
			del word[index+1]

	return ''.join(word)

def doublify_letters(word):
	''' whittle down repeat blocks of letters to 2 '''
	word = list(word)
	for index, letter in enumerate(word):
		while index+2 < len(word) and letter == word[index+1] and letter == word[index+2]:
			del word[index+2]

	return ''.join(word)


def get_alt_spellings(word):
	''' return a set of alternate spellings based on a key of common replacements '''
	word = list(word)
	lookup = {
		'a': ['i','o','e','a'],
		'e': ['i','a','ee','e'],
		'i': ['e','y','a','i'],
		'o': ['a','u','oo','o'],
		'u': ['o','u'],
		'y': ['i','y']
	}
	to_permutate = []
	for letter in word:
		if letter in lookup:
			to_permutate.append(lookup[letter])
		else:
			to_permutate.append(letter)

	permutations = list(itertools.product(*to_permutate))

	for index, p in enumerate(permutations):
		permutations[index] = ''.join(p)

	return set(permutations)

def spellcheck(word):
	if word in dictionary:
		return "Looks about right"

	else:
		word = word.lower()
		if word not in dictionary:
			word = doublify_letters(word)
		if word not in dictionary:
			word = uniquify_letters(word)
			alt_words = get_alt_spellings(word)
			alt_words = alt_words.union(get_alt_spellings(word)) # so peeeple -> people
			real_words = alt_words.intersection(dictionary)
			candidates = dict.fromkeys(real_words)
			for key in candidates:
				candidates[key] = dictionary[key]
			if candidates != []:
				for word in candidates:
					# print word
					word = max(candidates, key=candidates.get)

		if word not in dictionary:
			return "NO SUGGESTION"

		else:
			return "Did you mean: "+ word


dictionary = make_dictionary()

if test_words != []:
	for word in test_words:
		print "checking: " + word,
		print spellcheck(word.strip())

else:
	while True:
		word = raw_input("Word to check: ")
		print spellcheck(word)

