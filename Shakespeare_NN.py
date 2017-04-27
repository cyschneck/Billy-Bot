###########################################################################
# Shakespeare Sentiment Anaylsis

# Date: Jan. 2017

# Train a Hidden Markov Model with a collection of Shakespeare Sonnets and Plays
# Determine the sentiment state of a character based on their speech

###########################################################################
import random
import re
import string
from collections import Counter

from textblob import TextBlob

# TODO: remove character names, locations
punc = ['!', ',', '.', ':', '\'', ';', '*', '--']
character_names = ['claudius', 'hamlet', 'polonius', 'horatio', 'laertes',
					'voltimand', 'cornelius', 'rosencrantz', 'guildenstern',
					'osric', 'gentleman', 'priest', 'marcellus', 'bernardo',
					'francisco', 'reynaldo', 'players', 'clown1', 'clown2',
					'gertrude', 'ophelia', 'fortinbras', 'captain', 'ambassadors', 'ghost', 'other']


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

def basicNN():
	# basic nueral network trained for sentiment
	pass

def readingFileDict(filename):
	# reads in the file and returns a dictionay with headers and sequences: {header:sequence}
	fullList = []
	Charlist = []
	character_list = []
	speech_list = []

	append = fullList.append # avoid re-using append (to improve running time)
	with open(filename, "r") as given_file:
		seq = ''
		for line in given_file:
			line = line.rstrip('\n').replace(" ", "@").replace("\t", "@").replace("\r", "@") # replace spaces with known character and replace tabs
			if line.startswith('>'):
				line = line + ' '
				line = line.replace('>', ' >')
			append(line)
		seq = ''.join(fullList).upper()
		Charlist = seq.split()
		# Pulls out the character headers and speeches
		# By removing any extranous puncutation with predictable characters to be spliced

		# Returns the header sequence name
		append = seqlist.append # avoid re-using append (to improve running time)
		for element in Charlist:
			if ">" in element:
				element = element.replace("@", "")
				element = element.strip(">") # assumes all header/sequences starts with >
				append(element) # returns a list of  headers ['chrI', 'chrII', etc...]

		speech_list =  [x for x in Charlist if '>' not in x] # returns a list of sequence ['ATC', 'TGGC', etc..]
		speech_list = map(str.upper, speech_list) # convert all sequences to upper case for consitency

		for i in range(len(speech_list)): # remove extra @ left behind by replace and replace n with A (n = any ATCG)
			if '@' in speech_list[i]:
				new_value = speech_list[i].replace("@", "")
				speech_list[i] = new_value
		seq_dict = seqDictPairs(character_list, speech_list) # tuples of a pair's list and a dictionary {seq:gen}
	return seq_dict

def seqDictPairs(character_list, speech_list):
	# creates a dictionary between the charcter (header) and the associated speech {character:speech} dictionary
	char_spe_dict = {}
	char_spe_dict = zip(character_list, speech_list) # combine the two lists
	char_spe_dict = dict(char_spe_dict) # create new dictionary from the lists
	return char_spe_dict

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="flag format given as: -F <filename>")
	parser.add_argument('-F', '-filename', help="filename, given as .fasta")

	args = parser.parse_args()
	filename = args.F

	arguments = [filename]
	if None in arguments:
		if filename is None:
			print("filename not given")
			exit()
	
	char_speech_dict = readingFileDict(filename)
	words = "thus conscience does make cowards of us all"
	
	text = TextBlob(words)
	print(text.tags)
	print(text.words)
	print(text.sentiment)

	# iterate through all tokens for each speech (50 or 100 tokens in size max)
	# store sentiment in list for each character to graph
