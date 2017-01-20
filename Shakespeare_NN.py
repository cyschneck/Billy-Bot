# Shakespeare Neural Network (start Jan. 17, 2017)
# Train a Hidden Markov Model with a collection of Shakespeare Sonnets and Plays
# Generate a monolouge in any genre (Tragedy, History, Comedy) 75 words long
# Determine the sentimnt state of a character based on their speech
# Generation is based on a parsed argument --type (t, h, c)

import random
import re
import string
from collections import Counter

from textblob import TextBlob

# TODO: remove character names, locations
punc = ['!', ',', '.', ':', '\'', ';', '*', '--']
character_names = ["hamlet", "horatio"]


def printDict(dictionary):
	#print from largest to smallest frequency in order
	tmp = dictionary # print full dictionary in order from largest to smallest
	while(any(tmp)): #while tmp dictionary is not empty
		max_el = min(tmp, key=lambda key: tmp[key]) # return the largest dict value
		print("{0} = {1}".format(max_el, tmp[max_el])) #formating for print
		del tmp[max_el] # remove the largest element (for each round until none remain)

def translateFreqText(filename):
	#remove all characters and puncutation from text
	full_dictionary = []
	with open(filename, 'r') as given_file:
		words = given_file.read().lower() # translate text to lowercase
		words = words.translate(None, string.punctuation) # remove all puncation that is not part of a word (I'll)
		words = words.rsplit() # split into individual elements per word
	for word in words:
		full_dictionary.append(word) # populate the list
	
	freqDict = Counter(full_dictionary) # count the frequency of each word {word:#freq}
	
	#printDict(freqDict)
	return freqDict

def percentFreq(filename, freq_dict, total_words):
	## compute percentages
	probDict = {} # probabilty of each word appearing in the text

	for element in freq_dict.keys():
		frequency = (float(freq_dict[element]) / float(total_words))
		#print("%.6f" % frequency)
		probDict[element]=frequency
	
	#printDict(probDict)
	return probDict

'''
def markov_next(current, probDict):
    if current not in probDict:
        return random.choice(list(probDict.keys()))
    else:
        succProbs = probDict[current]
        randProb = random.random()
        currentProb = 0.0
        for succ in succProbs:
            currentProb += succProbs[succ]
            if randProb <= currentProb:
                return succ
        return random.choice(list(probDict.keys()))

def makePlay(current, probDict, length=75):
    play = [current]
    for words in range(length):
        play.append(markov_next(play[-1], probDict))
    new_word = ' '.join(str(p) for p in play)
    return new_word'''

if __name__ == '__main__':
	filename = 'hamlet_2bee.txt'
	freq_words = translateFreqText(filename) # word:#freq dictionary
	#printDict(freq_words)
	total_words = sum(freq_words.values()) # single number for total words
	#print(total_words)
	prob_word = percentFreq(filename, freq_words, total_words)
	#print(prob_word)
	#remove all characters and puncutation from text
	sent = []
	with open(filename, 'r') as given_file:
		words = given_file.read().lower() # translate text to lowercase
		words = words.translate(None, string.punctuation) # remove all puncation that is not part of a word (I'll)
		words = words.replace("'d", "ed")
	print(words)
	
	text = TextBlob(words)
	print(text.tags)
	print(text.words)
	print(text.sentiment)
