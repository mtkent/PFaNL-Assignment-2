# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen


#Marina Kent inf2a assignment 2

# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    NNSlist = []
    NNlist = []
    
    # will go through all of sentences.txt to look for nouns that are the same when singular and plural
    with open("sentences.txt", "r") as f:
        for line in f:
            list1 = line.split()  # splits up each item into (word|tag)
            for item in list1:
                list2 = item.split('|')  # split each word tag pair 
                
                # if tag is NNS, add it to a list
                if list2[1] == 'NNS':
                    NNSlist.append(list2[0])
                
                # if tag is NN, add it to another list
                elif list2[1] == 'NN':
                    NNlist.append(list2[0])

    # returns the intersection of the two lists - those that are NN and NNS
    return set(NNSlist).intersection(NNlist)


unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""

    if s in unchanging_plurals():
        toReturn = s # has no stem if unchanging
    elif re.match (".*(men)", s): #special rule for nouns
        s1 = s[:-3]
        s2 = s1 + "man"
        toReturn = s2
    elif re.match (".*(ays|eys|iys|oys|uys)", s): # rest is the same as verbs
        toReturn = s[:-1]
    elif re.match (".*(ies)", s):
        if (len(s) == 4):
            toReturn = s[:-1]
        else:
            s1 = s[:-3]
            s2 = s1 + "y"
            toReturn = s2 
    elif re.match(".*(oes|xes|ches|shes|sses|zzes)", s):
        toReturn = s[:-2]
    elif re.match (".*(!sses|!zzes|ses|zes)", s):
        toReturn = s[:-1]
    elif re.match(".*(!ies|!oes|!ses|!xes|!ches|!shes|es)", s):
        toReturn = s[:-1]
    elif re.match(".*(!ss|!xs|!ys|!zs|!chs|!shs|s)", s):
        toReturn = s[:-1]
    else:
        toReturn = ''

    return toReturn
          

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
   
    toReturn = [] # initialize a list to return

    # will go through tags and add to list as seen fit
    if wd in lx.getAll('P'):
        toReturn.append('P')
    if wd in lx.getAll('A'):
        toReturn.append('A')
    for item in function_words_tags:
        if item[0] == wd:
            toReturn.append(item[1])
    if (wd in lx.getAll('N')) or (noun_stem(wd) in lx.getAll('N')): # will check if stem is contained as well
        if wd in unchanging_plurals_list: # if unchanging, will be both singular and plural
            toReturn.append('Ns')
            toReturn.append('Np')
        elif (noun_stem(wd) == ''):  # if no stem, means is already singular
            toReturn.append('Ns')
        else:
            toReturn.append('Np')
    if (wd in lx.getAll('I')) or (verb_stem(wd) in lx.getAll('I')):
        if (verb_stem(wd) == ''): # same stem logic as nouns
            toReturn.append('Ip')
        else:
            toReturn.append('Is')
    if (wd in lx.getAll('T')) or (verb_stem(wd) in lx.getAll('T')):
        if (verb_stem(wd) == ''):  # again, same stem logic
            toReturn.append('Tp')
        else:
            toReturn.append('Ts')

    return toReturn  # returns the list of tags
          

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
