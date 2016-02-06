# Marina Kent Inf2a assignment 2

# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    # initialize the class
    def __init__(self):
        self.l = {'P':[], 'N':[], 'A':[], 'I':[], 'T':[]}

    # add will add an item to a specified list 
    def add(self, stem, cat):
        self.l[cat].append(stem)     

    # getAll will return a specified list without duplicates
    def getAll (self, cat):
        list = []
        
        for i in self.l[cat]:
            if i not in list:  
                list.append(i)
        return list
       

class FactBase:
    
    # initialize the list
    def __init__(self):
        self.u = {}
        self.b = {}
    
    # add a unary statement to a list
    def addUnary(self, pred, e1):
        if pred not in self.u:
            self.u[pred] = []
        self.u[pred].append(e1)

    # add a binary statement to a list
    def addBinary(self, pred, e1, e2):
        if pred not in self.b:
            self.b[pred] = []
        self.b[pred].append((e1,e2))

    # check a list to see if contains unary statement
    def queryUnary(self, pred, e1):
        if (e1 not in self.u[pred]):           
            return False
        return True;

    # check a list to see if contains a binary statement 
    def queryBinary(self, pred, e1, e2):
        if ((e1, e2) not in self.b[pred]):
            return False
        return True
        
        
import re
from nltk.corpus import brown 
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    
    # goes through rules outlined in handout
    if re.match ("has", s):
        toReturn =  'have'
    elif re.match (".*(ays|eys|iys|oys|uys)", s):
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

    # will check if original plural or creted singular verb is in the Brown corpus. 
    if ((s, 'VBZ') not in brown.tagged_words()):
        if ((toReturn, 'VB') not in brown.tagged_words()):
            return ''
        else: 
            return toReturn
    else:
        return toReturn
                    
    
def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.
