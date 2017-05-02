###########################################################################
# Shakespeare Sentiment Anaylsis

# Date: Jan. 2017

# Determine the sentiment state of a character based on their speech
# Compare the local emotion states of each character to the overall play's arc

###########################################################################
import random
import re
import csv
import string

from textblob import TextBlob

# list with all character options
hamlet_character_list = ['claudius', 'hamlet', 'polonius', 
						'horatio', 'laertes', 'rosencrantz', 'guildenstern',
						'osric', 'priest', 'marcellus', 'bernardo',
						'francisco', 'reynaldo', 'players', 'clownone',
						'clowntwo', 'gertrude', 'ophelia',
						'fortinbras', 'ghost', 'other']

# dictionary with the act and the number of scenes it has
hamlet_scene_breakdown = {1: [1, 2, 3, 4, 5], 2:[1, 2], 3:[1, 2, 3, 4], 4:[1, 2, 3, 4, 5, 6, 7], 5:[1, 2]}

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
		seq = ''.join(fullList).lower()
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
				new_value = speech_list[i].replace("@", " ") # keeps all spacing between paragraphs intacted
				speech_list[i] = new_value
			if ';' in speech_list[i]:
				new_value = speech_list[i].replace(";", ". ") # replace semi-colon into a sentence for tokenization (creates 'more' sentences)
				speech_list[i] = new_value
			if "'d" in speech_list[i]:
				new_value = speech_list[i].replace("'d", "ed") # corrrct 'old-english' to current for anaylsis
				speech_list[i] = new_value
			if '--' in speech_list[i]:
				new_value = speech_list[i].replace("--", "")
				speech_list[i] = new_value
			if '.' in speech_list[i]:
				new_value = speech_list[i].replace(".", ". ") # increase spacing for sentences
				speech_list[i] = new_value
		#print(speech_list)
		# check that no duplicates in keys occur
		#print("duplicates: {0}".format([x for n, x in enumerate(char_list) if x in char_list[:n]]))
		char_speech_dict = seqDictPairs(char_list, speech_list) # tuples of a pair's list and a dictionary {seq:gen}
		final_with_spaces_dict = addSpacestoSpeech(char_speech_dict)
	return final_with_spaces_dict

def addSpacestoSpeech(char_speech_dict):
	# removes spaces to parse correct, but adds them back here
	for key in char_speech_dict:
		if "#" in char_speech_dict[key]:
			with_spaces = char_speech_dict[key].replace("#", " ")
			char_speech_dict[key] = with_spaces
	return char_speech_dict

def seqDictPairs(header_list, sequence_list):
	# creates a dictionary between the sequence (header) and the associated genome {seq:genome} dictionary
	# takes in the header list and the sequence list to combine into a single diectionary that can be searched
	# setting up sequence genome dictionary
	seq_gen_dict = {}
	seq_gen_dict = zip(header_list, sequence_list) # combine the two lists
	seq_gen_dict = dict(seq_gen_dict) # create new dictionary from the lists
	return seq_gen_dict

def determineFocus(character_value, act_value, scene_value):
	# prints the focus of the play
	if character_value is None:
		if act_value is None:
			print("generate full play with full cast")
		else:
			if scene_value is None:
				print("generate act {0}, for all characters".format(act_value))
			else:
				print("generate scene {0}, in act {1}".format(scene_value, act_value))
	else:
		if act_value is None:
			print("generate full play for {0}".format(character_value))
		else:
			if scene_value is None:
				print("generate act {1}, for {1}".format(act_value, character_value))
			else:
				print("generate scene {0}, in act {1} for {2}".format(scene_value, act_value, character_value))

def findMissingName(list_character, char_dict):
	# find headers that are not being included (debugging)
	missing_ch = []
	for key in char_dict:
		found = False
		for character_type in list_character:
			if character_type in key:
				found = True
				#print("found: {0} in {1}".format(key, character_type))
		if not found:
			missing_ch.append(key)
	if len(missing_ch) > 0:
		print("\nmissing")
		for ch in missing_ch:
			print("not found: {0}".format(ch))

def determineSentiment(sent_dict):
	# takes in a dictionary or sub-dictionary to return the sentiment in a list
	final_sent_dict = {}
	sentence_list = []
	for speech in sent_dict:
		text_sent = TextBlob(sent_dict[speech])
		#text_tag = text_sent.tags
		for sentence in text_sent.sentences:
			final_sent_dict[speech] = sentence.sentiment
	final_sent_dict["_average"] = text_sent.sentiment # beginning of an ordered dict
	return final_sent_dict

def updateSentimentifNeutral(speech_sentence):
	# if the sentence is neutral, update to attribute sentiment based on key words
	# example: villian -> negative
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="flag format given as: -F <filename>")
	parser.add_argument('-F', '-filename', help="filename, given as .fasta")
	parser.add_argument('-A', '-act', help="act to analysis") # optional argument
	parser.add_argument('-S', '-scene', help="specific scene from act") # optional argument
	parser.add_argument('-C', '-character', help="character to analysis") # optional argument

	args = parser.parse_args()
	filename = args.F
	# below are optional arguments, if none are given, runs through entire play, for all characters
	act_value = args.A # if no scene is specified, runs through the entire act
	scene_value = args.S # must have an associated act_value
	character_value = args.C # if no act/scene is specified, runs for the entire play

	arguments = [filename] # required arguments
	if None in arguments:
		if filename is None:
			print("filename not given")
			exit()

	if (scene_value is not None) and (act_value is None):
		print("scene needs to be given in association with a specific act")
		exit()

	if act_value is not None:
		if type(act_value) is str: # if the given value is a string
			if act_value.lower() == 'one' or act_value == '1' or act_value.lower() == 'i':
				act_value = 1
			elif act_value.lower() == 'two' or act_value == '2'  or act_value.lower() == 'ii':
				act_value = 2
			elif act_value.lower() == 'three' or act_value == '3' or act_value.lower() == 'iii':
				act_value = 3
			elif act_value.lower() == 'four' or act_value == '4' or act_value.lower() == 'iv':
				act_value = 4
			elif act_value.lower() == 'five' or act_value == '5' or act_value.lower() == 'v':
				act_value = 5
			else:
				print("act must be between 1-5, {0} is not a valid argument".format(act_value))
				exit()
		else:
				print("act must be between 1-5, {0} is not a valid argument".format(act_value))
				exit()

	if scene_value is not None:
		if type(scene_value) is str: # if the given value is a string
			if scene_value.lower() == 'one' or scene_value == '1' or scene_value.lower() == 'i':
				scene_value = 1
			elif scene_value.lower() == 'two' or scene_value == '2'  or scene_value.lower() == 'ii':
				scene_value = 2
			elif scene_value.lower() == 'three' or scene_value == '3' or scene_value.lower() == 'iii':
				scene_value = 3
			elif scene_value.lower() == 'four' or scene_value == '4' or scene_value.lower() == 'iv':
				scene_value = 4
			elif scene_value.lower() == 'five' or scene_value == '5' or scene_value.lower() == 'v':
				scene_value = 5
			elif scene_value.lower() == 'six' or scene_value == '6' or scene_value.lower() == 'vi':
				scene_value = 6
			elif scene_value.lower() == 'seven' or scene_value == '7' or scene_value.lower() == 'vii':
				scene_value = 7
			else:
				print("scene must be between 1-7, {0} is not a valid argument".format(scene_value))
				exit()
		else:
				print("other scene must be between 1-7, {0} is not a valid argument".format(scene_value))
				exit()

	if scene_value is not None and scene_value not in hamlet_scene_breakdown[act_value]: # scene must be a valid number for a given act
		print("Act {0} has {1} scenes, {2} is not a valid argument".format(act_value, max(hamlet_scene_breakdown[act_value]), scene_value))
		exit()

	# TODO: give the option for 2 characters
	if character_value is not None:
		character_value = character_value.lower() # change names to lowercase for consitency
		if character_value not in hamlet_character_list:
			print("{0} is not a valid argument, if not included, additional characters are listed under 'other'\n".format(character_value))
			print("Other options include:")
			for char in hamlet_character_list:
				print(char)
			exit()

	char_speech_dict = readingFileDict(filename)

	# determine what the focus of the graph is
	#determineFocus(character_value, act_value, scene_value)

	# creates dictionaries with {characterACTSCENE_SPEECH: "speech"} and sub_dictionaries
	if character_value is not None:
		if act_value is not None:
			if scene_value is not None:
				regex_total = re.compile(r'{0}{1}{2}_\d'.format(character_value, act_value, scene_value))
			else:
				regex_total = re.compile(r'{0}{1}\d_\d'.format(character_value, act_value))
		else:
			regex_total = re.compile(r'{0}\d_\d'.format(character_value))
	else:
		if act_value is not None:
			if scene_value is not None:
				regex_total = re.compile(r'{0}{1}_\d'.format(act_value, scene_value))
			else:
				regex_total = re.compile(r'{0}\d_\d'.format(act_value))

	focus_dict = { k:v for k, v in char_speech_dict.items() if bool(re.search(regex_total, k)) } # dictionary that should have been generated

	if len(focus_dict) == 0: # character does not exist in the scene they are called for (exit)
		print("character {0} does not exist in this range".format(character_value))
		exit()

	print(focus_dict.keys())

	#final_graph_dict = determineSentiment(fortinbras_parts)
	#print(final_graph_dict)
	#ordered_final_sent = sorted(final_graph_dict.keys())
	#print(ordered_final_sent)
	# put dict in order: ordered_sent_list = sorted(sent_dict.keys())

	# output in csv
	output_filename = 'HAMLET_'
	if character_value is None:
		if act_value is None:
			output_filename += 'full.csv'
		else:
			if scene_value is None:
				output_filename += 'A{0}.csv'.format(act_value)
			else:
				output_filename += 'A{0}-S{1}.csv'.format(act_value, scene_value)
	else:
		if act_value is None:
			output_filename += '{0}.csv'.format(character_value)
		else:
			if scene_value is None:
				output_filename += '{0}-A{1}.csv'.format(character_value, act_value)
			else:
				output_filename += '{0}-A{1}-S{2}.csv'.format(character_value, act_value, scene_value)

	print(output_filename)
	'''
	with open(output_filename, 'w+') as given_sent:
		fieldnames = ['character', 'sentiment']
		writer = csv.DictWriter(given_sent, fieldnames=fieldnames)
		
		writer.writeheader() 
		for key, value in final_graph_dict.items():
			writer.writerow({'character': '{0}'.format(key), 'sentiment': '{0}'.format(value)})
	'''
	
	# include when a character enters and exit the play, how often they speech (frequency/total play)
	# if user wants the sentiment for an act that a character doesn't exist, throw error (exit)
	# fix bug in ordered where _6 is bigger than _58
