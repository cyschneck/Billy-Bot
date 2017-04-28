###########################################################################
# Shakespeare Sentiment Anaylsis

# Date: Jan. 2017

# Determine the sentiment state of a character based on their speech
# Compare the local emotion states of each character to the overall play's arc

###########################################################################
import random
import re
import string
from collections import Counter

from textblob import TextBlob

punc = ['!', ',', '.', ':', '\'', ';', '*', '--']
character_names = ['claudius', 'hamlet', 'polonius', 
					'horatio', 'laertes', 'voltimand',
					'cornelius', 'rosencrantz', 'guildenstern',
					'osric', 'gentleman', 'priest',
					'marcellus', 'bernardo', 'francisco',
					'reynaldo', 'players', 'clownone',
					'clowntwo', 'gertrude', 'ophelia',
					'fortinbras', 'captain', 'ambassadors',
					'ghost', 'other']
########################################################################
## SETTING UP THE DICTIONARIES FROM THE GIVEN FILES

def readingFileDict(filename):
	# reads in the file and returns a dictionay with headers and sequences: {header:sequence}
	fullList = []
	characterList = []
	char_list = []
	speech_list = []

	append = fullList.append # avoid re-using append (to improve running time)
	with open(filename, "r") as given_file:
		seq = ''
		for line in given_file:
			line = line.rstrip('\n').replace(" ", "#").replace("\t", "@").replace("\r", "@") # replace spaces with known character and replace tabs
			if line.startswith('>'):
				line = line + ' '
				line = line.replace('>', ' >')
			append(line)
		seq = ''.join(fullList).upper()
		characterList = seq.split()
		# Pulls out the sequences and genomes
		# By removing any extranous puncutation with predicatble characters to be spliced

		# Returns the header sequence name
		append = char_list.append # avoid re-using append (to improve running time)
		for element in characterList:
			if ">" in element:
				element = element.replace("@", "")
				element = element.strip(">") # assumes all header/sequences starts with >
				append(element) # returns a list of  headers ['chrI', 'chrII', etc...]
		#print(char_list)
		speech_list =  [x for x in characterList if '>' not in x] # returns a list of sequence ['ATC', 'TGGC', etc..]
		speech_list = map(str.lower, speech_list) # convert all sequences to upper case for consitency

		for i in range(len(speech_list)): # remove extra @ left behind by replace and replace n with A (n = any ATCG)
			if '@' in speech_list[i]:
				new_value = speech_list[i].replace("@", "")
				speech_list[i] = new_value
		#print(speech_list)
		# check that no duplicates in keys occur
		#duplicates = [x for n, x in enumerate(char_list) if x in char_list[:n]]
		char_speech_dict = seqDictPairs(char_list, speech_list) # tuples of a pair's list and a dictionary {seq:gen}
		final_with_spaces_dict = addSpacestoSpeech(char_speech_dict)
	return final_with_spaces_dict


def seqDictPairs(header_list, sequence_list):
	# creates a dictionary between the sequence (header) and the associated genome {seq:genome} dictionary
	# takes in the header list and the sequence list to combine into a single diectionary that can be searched
	# setting up sequence genome dictionary
	seq_gen_dict = {}
	seq_gen_dict = zip(header_list, sequence_list) # combine the two lists
	seq_gen_dict = dict(seq_gen_dict) # create new dictionary from the lists
	return seq_gen_dict

def addSpacestoSpeech(char_speech_dict):
	# removes spaces to parse correct, but adds them back here
	for key in char_speech_dict:
		if "#" in char_speech_dict[key]:
			with_spaces = char_speech_dict[key].replace("#", " ")
			char_speech_dict[key] = with_spaces
	return char_speech_dict

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

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="flag format given as: -F <filename>")
	parser.add_argument('-F', '-filename', help="filename, given as .fasta")
	#parser.add_argument('-C', '-character', help="character to analysis")

	args = parser.parse_args()
	filename = args.F

	arguments = [filename]
	if None in arguments:
		if filename is None:
			print("filename not given")
			exit()
	
	char_speech_dict = readingFileDict(filename)
	for key in sorted(char_speech_dict)[:50]:
		print("{0}:{1}".format(key, char_speech_dict[key]))
	'''
	words = "thus conscience does make cowards of us all"
	text = TextBlob(words)
	print(text.tags)
	print(text.words)
	print(text.sentiment)
	'''

	# iterate through all tokens for each speech (50 or 100 tokens in size max)
	# store sentiment in list for each character to graph
