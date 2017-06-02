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
import operator

from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier # update sentiment, if textblob returns neutral
import matplotlib.pyplot as plt # graphing
import numpy as np # for np.nan = 'nan' to graph in color

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
				new_value = speech_list[i].replace("--", " ")
				speech_list[i] = new_value
			if '.' in speech_list[i]:
				new_value = speech_list[i].replace(".", ". ") # increase spacing for sentences
				speech_list[i] = new_value
			if ',' in speech_list[i]:
				new_value = speech_list[i].replace(",", ", ") # increase spacing for commas
				speech_list[i] = new_value
			if '?' in speech_list[i]:
				new_value = speech_list[i].replace("?", "? ") # increase spacing for ?'s
				speech_list[i] = new_value

		#print(speech_list)
		# check that no duplicates in keys occur
		#print("duplicates: {0}".format([x for n, x in enumerate(char_list) if x in char_list[:n]]))
		char_speech_dict = seqDictPairs(char_list, speech_list) # tuples of a pair's list and a dictionary {seq:gen}
		final_with_spaces_dict = addSpacestoSpeech(char_speech_dict)
	# returns the final dictionary with the header and the speech associated, also return the headers in the order they first appeared
	return (final_with_spaces_dict, char_list)

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

def sortedSpeakingInOrder(given_list, deli_num):
	# return the list of speaking roles in order

	# order the keys in the order they appear in the play
	split_keys = [order.split('_') for order in given_list]
	# breaks hamlet51_1 => ['hamlet51', '1']
	sorted_lines = sorted(split_keys, key=lambda x:int(x[deli_num])) 
	# returns the list of character lines in order [['hamlet52', '1'], ['hamlet51, '2']]
	sorted_keys = ['_'.join(order) for order in sorted_lines]
	
	# returns to a single list: ['hamlet52_1', 'hamlet52_2'] in order
	return sorted_keys

def characterInfo(character_name, full_play_dictionary):
	# include when a character enters and exit the play, how often they speech (frequency/total play)
	pass

def determineSentiment(sent_dict):
	# takes in a dictionary or sub-dictionary to return the sentiment in a list
	final_sent_dict = {}
	sentence_list = []
	for speech in sent_dict:
		text_sent = TextBlob(sent_dict[speech])
		#text_tag = text_sent.tags
		counter = 1
		for sentence in text_sent.sentences:
			#print(speech)
			final_sent_dict[speech + '_' + str(counter)] = (sentence.sentiment, sentence)
			counter += 1 # each sub-sentence in a speech has it's own dictionary key
	final_sent_dict["_average"] = text_sent.sentiment # beginning of an ordered dict
	return final_sent_dict

def trainSentiment():
	# if the sentence is neutral, update to attribute sentiment based on key words
	# example: villian -> negative, dying -> negative, etc...
	# https://textblob.readthedocs.io/en/dev/classifiers.html#classifiers

	# train classifers on actual hamlet data
	hamlet_train = [
	# act 1
		('this dreaded sight', 'neg'),
		('o god!', 'neg'),
		('o fie!', 'neg'),
		('break my heart,  for i must hold my tongue!', 'neg'),
		('funeral', 'neg'),
		('he was a man,  take him for all in all, i shall not look upon his like again', 'neg'),
		('i doubt some foul play would the night were come!', 'neg'),
		('foul deeds will rise', 'neg'),
		('pooh!', 'neg'),
		('angels and ministers of grace defend us!', 'neg'),
		('you shall not go', 'neg'),
		('hold off your hands', 'neg'),
		('my fate cries out' , 'neg'),
		("i'll make a ghost of him that lets me" , 'neg'),
		('something is rotten in the state of denmark', 'neg'),
		('harrow up thy soul', 'neg'),
		('revenge', 'neg'),
		('incest', 'neg'),
		('adulterate', 'neg'),
		('beast', 'neg'),
		('lust', 'neg'),
		('a serpent stung me', 'neg'),
		('villain', 'neg'),
		('perturbed spirit!', 'neg')
	]

	hamlet_test = [
	# act 2
		('dishonour', 'neg'),
		('taints of liberty', 'neg'),
		('flash and outbreak of a fiery mind', 'neg'),
		('falsehood', 'neg'),
		('fouled', 'neg'),
		('piteous', 'neg'),
		('i do not know', 'neg'),
		('i do fear it', 'neg'),
		('madness wherein now he raves', 'neg'),
		('madness', 'neg'),
		('indifferent children of the earth', 'neg'),
		('beggars bodies', 'neg'),
		('murder', 'neg'),
		('that he should weep for her?', 'neg'),
		('am i a coward?', 'neg'),
		('who calls me villain?', 'neg'),
	]
	cl = NaiveBayesClassifier(hamlet_train)
	return cl

def updateSentimentifNeutral(sentence, speech_dict, speech_neutral):
	# update sentiment based on training data
	cl = trainSentiment()
	updated_polarity = 0.0
	negative_sent = -0.2
	postive_sent = 0.2
	#print(speech_dict[sentence][1])
	
	classifed_value = cl.classify(sentence)
	#print(classifed_value)
	if classifed_value == 'neg':
		updated_polarity = negative_sent
	else:
		updated_polarity = postive_sent
	#'Sentiment(polarity=0.0, subjectivity=0.0)'
	#print(updated_polarity)
	return updated_polarity

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

	if character_value is not None:
		character_value = character_value.lower() # change names to lowercase for consitency
		if character_value not in hamlet_character_list:
			print("{0} is not a valid argument, if not included, additional characters are listed under 'other'\n".format(character_value))
			print("Other options include:")
			for char in hamlet_character_list:
				print(char)
			exit()

	fileFastaRead = readingFileDict(filename)
	char_speech_dict = fileFastaRead[0] # full dictionary
	ordered_headers_list = fileFastaRead[1] # headers in the order they appear (used if no character is speficially called for)

	# determine what the focus of the graph is (print statements)
	#determineFocus(character_value, act_value, scene_value)

	# creates dictionaries with {characterACTSCENE_SPEECH: "speech"} and sub_dictionaries
	if character_value is not None:
		if act_value is not None:
			if scene_value is not None:
				regex_total = re.compile(r'{0}{1}{2}_\d'.format(character_value, act_value, scene_value))
			else:
				regex_total = re.compile(r'{0}{1}\d_\d'.format(character_value, act_value))
		else:
			regex_total = re.compile(r'{0}\d\d_\d'.format(character_value))
	else:
		if act_value is not None:
			if scene_value is not None:
				regex_total = re.compile(r'[a-z]+{0}{1}_\d'.format(act_value, scene_value))
			else:
				regex_total = re.compile(r'[a-z]+{0}\d_\d'.format(act_value))
		#else:
		#	regex_total = re.compile(r'[a-z]+\d_\d')

	if character_value is None and scene_value is None and act_value is None:
		focus_dict = char_speech_dict
	else:
		focus_dict = { k:v for k, v in char_speech_dict.items() if bool(re.search(regex_total, k)) } # dictionary that should have been generated
	#print(focus_dict)

	if len(focus_dict) == 0: # character does not exist in the scene they are called for (exit)
		print("character {0} does not exist in this range".format(character_value))
		exit()

	if character_value is not None:
		# return the list of speaking roles in order
		#print(focus_dict.keys())
		sorted_speaking = sortedSpeakingInOrder(focus_dict.keys(), 1) # based on 'hamlet15_2' where 2 is the second time they spoke

		sentiment_focus_dict = determineSentiment(focus_dict) # dictionary for sentence: polarity (includes the given speech as a tuple)

		sent_sentences_dict = {} 
		# creates a dictionary that stores the sub-sentences for each speaking time {hamlet15_24:['hamlet15_24_1', 'hamlet15_24_2', 'hamlet15_24_3']}
		lst_speaking = []
		total = []
		for speaking_num in sorted_speaking:
			for key, value in sentiment_focus_dict.iteritems():
				regex_header = re.compile(r'{0}_\d+'.format(speaking_num))
				total.append(key)
				if bool(re.search(regex_header, key)): # create a dictionary that associates a speech with its sentences
					lst_speaking.append(key)
			sent_sentences_dict[speaking_num] = lst_speaking
			lst_speaking = []
		#print("\n")
		for key, value, in sent_sentences_dict.iteritems():
			sorted_speaking_sentences = sortedSpeakingInOrder(value, 2)
			#print(key)
			#print(sorted_speaking_sentences)
			#print(sent_sentences_dict[key])
			sent_sentences_dict[key] = sorted_speaking_sentences # returns the order of the setences for a speech in order they appear
			# example: 'hamlet15_2_4', where 4 is the fourth sentence in the second time they spoke
	else: # specific character is not included
		# ordered_headers_list hold the values in order that they appear for the whole play
		#print(focus_dict.keys())
		sorted_speaking = []
		for order_head in ordered_headers_list:
			if order_head in focus_dict:
				sorted_speaking.append(order_head)
		#print(sorted_speaking)
		sentiment_focus_dict = determineSentiment(focus_dict) # dictionary for sentence: polarity (includes the given speech as a tuple)

		sent_sentences_dict = {} 
		# creates a dictionary that stores the sub-sentences for each speaking time {hamlet15_24:['hamlet15_24_1', 'hamlet15_24_2', 'hamlet15_24_3']}
		lst_speaking = []
		total = []
		for speaking_num in sorted_speaking:
			for key, value in sentiment_focus_dict.iteritems():
				regex_header = re.compile(r'{0}_\d+'.format(speaking_num))
				total.append(key)
				if bool(re.search(regex_header, key)): # create a dictionary that associates a speech with its sentences
					lst_speaking.append(key)
			sent_sentences_dict[speaking_num] = lst_speaking
			lst_speaking = []
		#print("\n")
		for key, value, in sent_sentences_dict.iteritems():
			sorted_speaking_sentences = sortedSpeakingInOrder(value, 2)
			#print(key)
			#print(sorted_speaking_sentences)
			#print(sent_sentences_dict[key])
			sent_sentences_dict[key] = sorted_speaking_sentences # returns the order of the setences for a speech in order they appear
			# example: 'hamlet15_2_4', where 4 is the fourth sentence in the second time they spoke
		#sentiment_focus_dict = determineSentiment(focus_dict) # dictionary for sentence: polarity (includes the given speech as a tuple)

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
			output_filename += 'full_{0}.csv'.format(character_value)
		else:
			if scene_value is None:
				output_filename += '{0}-A{1}.csv'.format(character_value, act_value)
			else:
				output_filename += '{0}-A{1}-S{2}.csv'.format(character_value, act_value, scene_value)

	print(output_filename)

	print("\n")
	# with the sentiment for each sentence (sentiment_focus_dict), the order they appear (sorted_speaking for overall, and sent_sentences_dict for sentences), print to a graph


	with open(output_filename, 'w+') as given_sent:
		fieldnames = ['id', 'speaker_header', 'polarity', 'subjectivity']
		writer = csv.DictWriter(given_sent, fieldnames=fieldnames)
		
		writer.writeheader() 
		id_value = 1
		for overall_speech in sorted_speaking:
			for sentence in sent_sentences_dict[overall_speech]:
				#print('internal senetence {0}'.format(sentence))
				polarity = sentiment_focus_dict[sentence][0].polarity
				subjectivity = sentiment_focus_dict[sentence][0].subjectivity
				if polarity != 0.0 and subjectivity != 0.0:
					writer.writerow({'id': '{0}'.format(id_value), 'speaker_header': '{0}'.format(sentence), 'polarity': '{0}'.format(polarity), 'subjectivity': '{0}'.format(subjectivity)})
					id_value += 1
				# update any sentiment values that are considered nuetral
				if polarity == 0.0:
					updated_polarity = updateSentimentifNeutral(sentence, sentiment_focus_dict, sentiment_focus_dict[sentence][0])
					updated_polarity = 0.0
					writer.writerow({'id': '{0}'.format(id_value), 'speaker_header': '{0}'.format(sentence), 'polarity': '{0}'.format(updated_polarity), 'subjectivity': '{0}'.format(subjectivity)})
					id_value += 1


	chart_title = ''
	if character_value is None:
		if act_value is None:
			chart_title += 'Full Play'
		else:
			if scene_value is None:
				chart_title += 'Act {0}'.format(act_value)
			else:
				chart_title += 'Act {0} Scene {1}'.format(act_value, scene_value)
	else:
		if act_value is None:
			chart_title += 'Full Play for {0}'.format(character_value.title()) # captilze the first letter of the same
		else:
			if scene_value is None:
				chart_title += 'Act {0} for {1}'.format(act_value, character_value.title())
			else:
				chart_title += 'Act {0} Scene {1} for {2}'.format(act_value, scene_value, character_value.title())

	line_stamp = []
	sent_polarity = []
	with open(output_filename) as results:
		reader = csv.DictReader(results, delimiter=',')
		for row in reader:
			line_stamp.append(row['id'])
			sent_polarity.append(row['polarity'])

	overall_avg = [float(n) for n in sent_polarity if n != 0]
	overall_avg = sum(overall_avg)/len(overall_avg)
	print(overall_avg)
	
	plt.figure("Polarity over Time")
	plt.title("{0}".format(chart_title))
	plt.ylabel("Polarity [-1.0, 1.0]")
	plt.xlabel("Lines")

	avg_line = [(float(a)+float(b))/2 for a, b in zip(sent_polarity[:], sent_polarity[1:])]
	avg_line.append((float(sent_polarity[-2])+float(sent_polarity[-1]))/2)

	pos_pol = []
	neg_pol = []
	zed_pol = []
	# color classify values (red = postive, blue = negative, grey = zero)
	for value in sent_polarity:
		if float(value) < 0:
			neg_pol.append(value)
			pos_pol.append(np.nan)
			zed_pol.append(np.nan)
		elif float(value) > 0:
			pos_pol.append(value)
			neg_pol.append(np.nan)
			zed_pol.append(np.nan)
		else:
			zed_pol.append(value)
			neg_pol.append(np.nan)
			pos_pol.append(np.nan)

	#print(pos_pol)
	#print(neg_pol)
	#line, plt.plot([0]*len(sent_polarity), '-')
	#plt.plot([0]*len(sent_polarity), linestyle=':', color='black')
	plt.plot(line_stamp, avg_line, color='k', linestyle=':') # average line
	plt.scatter(line_stamp, pos_pol, color = 'r')
	plt.scatter(line_stamp, neg_pol,  color = 'b')
	plt.scatter(line_stamp, zed_pol, color = '0.75')
	plt.show()

	# include when a character enters and exit the play, how often they speech (frequency/total play)
	# fix spacing after ; and with carriage returns (needs space)
