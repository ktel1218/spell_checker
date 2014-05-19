# Final step: Write a second program that generates words with spelling mistakes of the above form, starting with correctly spelled English words. Pipe its output into the first program and verify that there are no occurrences of "NO SUGGESTION" in the output.

import random, sys

dictionary = list(open('words.txt', 'r')) # from /usr/share/dict/words


lookup = {
	'a': ['a','e','o','i'],
	'e': ['e','a','i'],
	'i': ['i','a','y','e'],
	'o': ['o','u','a'],
	'u': ['u','o'],
	'y': ['y','i'],
}

def duplicate_letters(word):
	rand_index = random.randint(0, len(word) - 1)
	no_of_duplications = random.randint(2,10)
	return word[:rand_index] + (word[rand_index] * no_of_duplications) + word[(rand_index + 1) :]

def capitalize_letters(word):
	word = list(word)
	no_of_capitalizations = random.randint(0, len(word))
	for i in range(no_of_capitalizations):
		index = random.randint(0, len(word) - 1)
		word[index] = word[index].upper()
	return ''.join(word)

def switch_vowels(word):
	word = list(word)
	for index, letter in enumerate(word):
		if letter in lookup:
			rand_index = random.randint(0, len(lookup[letter])-1)
			word[index] = lookup[letter][rand_index]
	return ''.join(word)

# def test_spell_checker()
# 	while True:
def generate_garbage():
	rand_word = dictionary[random.randint(0, len(dictionary)-1)].strip()
	print rand_word
	return capitalize_letters(duplicate_letters(switch_vowels(rand_word)))
