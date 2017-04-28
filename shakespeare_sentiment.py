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

def partsCharacter(character_name, char_speech_dict):
	# break apart entire (unparsed) dictionary into sub-dictionaries for each character
	character_name_parts = { k:v for k, v in char_speech_dict.items() if character_name in k }
	#print("{0} = {1}".format(character_name, len(character_name_parts)))
	return character_name_parts

def partAct(act_num, char_speech_dict):
	# break apart entire (unparsed) dictionary into sub-dictionaries for each act
	regex_act = re.compile(r'{0}\d_\d'.format(act_num))
	act_parts = { k:v for k, v in char_speech_dict.items() if bool(re.search(regex_act, k)) }
	return act_parts

def partScene(scene_num, act_dict):
	# break apart act dictionary into sub-dictionaries for each scene
	regex_scene = re.compile(r'\d{0}_\d'.format(scene_num))
	scene_parts = { k:v for k, v in act_dict.items() if bool(re.search(regex_scene, k)) }
	return scene_parts

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

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="flag format given as: -F <filename>")
	parser.add_argument('-F', '-filename', help="filename, given as .fasta")
	#parser.add_argument('-A', '-act', help="act to analysis")
	#parser.add_argument('-AS', '-act_scene', help="act and specific scene")
	#parser.add_argument('-P', '-play_to_breakdown', help="default set to hamlet")


	args = parser.parse_args()
	filename = args.F

	arguments = [filename]
	if None in arguments:
		if filename is None:
			print("filename not given")
			exit()
	
	char_speech_dict = readingFileDict(filename)

	# TO DO: go through and remove characters that are not being used as headers
	hamlet_parts = partsCharacter('hamlet', char_speech_dict)
	claudius_parts = partsCharacter('claudius', char_speech_dict)
	polonius_parts = partsCharacter('polonius', char_speech_dict)
	horatio_parts = partsCharacter('horatio', char_speech_dict)
	laertes_parts = partsCharacter('laertes', char_speech_dict)
	voltimand_parts = partsCharacter('voltimand', char_speech_dict)
	cornelius_parts = partsCharacter('cornelius', char_speech_dict)
	rosencrantz_parts = partsCharacter('rosencrantz', char_speech_dict)
	guildenstern_parts = partsCharacter('guildenstern', char_speech_dict)
	osric_parts = partsCharacter('osric', char_speech_dict)
	gentleman_parts = partsCharacter('gentleman', char_speech_dict)
	marcellus_parts = partsCharacter('marcellus', char_speech_dict)
	bernardo_parts = partsCharacter('bernardo', char_speech_dict)
	francisco_parts = partsCharacter('francisco', char_speech_dict)
	reynaldo_parts = partsCharacter('reynaldo', char_speech_dict)
	players_parts = partsCharacter('players', char_speech_dict)
	clownone_parts = partsCharacter('clownone', char_speech_dict)
	gertrude_parts = partsCharacter('gertrude', char_speech_dict)
	clowntwo_parts = partsCharacter('clowntwo', char_speech_dict)
	ophelia_parts = partsCharacter('ophelia', char_speech_dict)
	fortinbras_parts = partsCharacter('fortinbras', char_speech_dict)
	captain_parts = partsCharacter('captain', char_speech_dict)
	ambassadors_parts = partsCharacter('ambassadors', char_speech_dict)
	ghost_parts = partsCharacter('ghost', char_speech_dict)
	other_parts = partsCharacter('other', char_speech_dict)
	
	'''
	total = len(hamlet_parts) + len(claudius_parts) + len(polonius_parts) + len(horatio_parts)
	total = total + len(laertes_parts) + len(voltimand_parts) + len(cornelius_parts)
	total = total + len(rosencrantz_parts) + len(guildenstern_parts) + len(osric_parts)
	total = total + len(gentleman_parts) + len(marcellus_parts) + len(bernardo_parts)
	total = total + len(francisco_parts) + len(reynaldo_parts) + len(players_parts)
	total = total + len(clownone_parts) + len(gertrude_parts) + len(clowntwo_parts)
	total = total + len(ophelia_parts) + len(fortinbras_parts) + len(captain_parts)
	total = total + len(ambassadors_parts) + len(ghost_parts) + len(other_parts)
	print(len(char_speech_dict))
	print("total: {0}".format(total))
	print("Found All: {0}".format(total == len(char_speech_dict)))
	findMissingName(character_names, char_speech_dict)
	'''
	#for key in sorted(char_speech_dict)[:50]:
	#	print("{0}:{1}".format(key, char_speech_dict[key]))


	act_one = partAct(1, char_speech_dict)
	act_one_scene_one = partScene(1, act_one)
	act_one_scene_two = partScene(2, act_one)
	act_one_scene_three = partScene(3, act_one)
	act_one_scene_four = partScene(4, act_one)
	act_one_scene_five= partScene(5, act_one)
	'''
	total = len(act_one_scene_one) + len(act_one_scene_two) + len(act_one_scene_three) + len(act_one_scene_four) + len(act_one_scene_five)
	print("total: {0}".format(total))
	print("Found All: {0}".format(total == len(act_one)))
	'''
	#TODO: break apart other acts for scenes and test that length of combined is the act
	act_two = partAct(2, char_speech_dict)
	act_three = partAct(3, char_speech_dict)
	act_four = partAct(4, char_speech_dict)
	act_five = partAct(5, char_speech_dict)

	'''
	print(len(act_one))
	print(len(act_two))
	print(len(act_three))
	print(len(act_four))
	print(len(act_five))
	total = len(act_one) + len(act_two) + len(act_three) + len(act_four) + len(act_five)
	print("total: {0}".format(total))
	print("Found All: {0}".format(total == len(char_speech_dict)))
	'''

	'''
	words = "thus conscience does make cowards of us all"
	text = TextBlob(words)
	print(text.tags)
	print(text.words)
	print(text.sentiment)
	'''
########################################
	# iterate through all tokens for each speech (50 or 100 tokens in size max)
	# store sentiment in list for each character to graph
