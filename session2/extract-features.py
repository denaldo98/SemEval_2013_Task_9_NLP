#! /usr/bin/python3

from lib2to3.pgen2 import token
import sys
import re
#import nltk
#nltk.download('stopwords')
from os import listdir

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 

   
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    ## word_tokenize splits words, taking into account punctuations, numbers, etc.
    for t in word_tokenize(txt):
        ## keep track of the position where each token should appear, and
        ## store that information with the token
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)

    ## tks is a list of triples (word,start,end)
    return tks


## --------- get tag ----------- 
##  Find out whether given token is marked as part of an entity in the XML

def get_tag(token, spans) :
   (form,start,end) = token
   for (spanS,spanE,spanT) in spans :
      if start==spanS and end<=spanE : return "B-"+spanT
      elif start>=spanS and end<=spanE : return "I-"+spanT

   return "O"
 
## --------- Feature extractor ----------- 
## -- Extract features for each token in given sentence

# generate camel-case version of a string
def camel_case(s):
  s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
  if len(s) == 0: return s
  return ''.join([s[0].lower(), s[1:]])

# dictionary containing information from external knowledge resources
external = {}

# build the dictionary 
path = "../TaskData/resources/HSDB.txt" # read the HSDB file
with open(path, encoding="utf8") as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug" # add drug into the dictionary

path = "../TaskData/resources/DrugBank.txt" # read the DrugBank file
with open(path, encoding="utf8") as h :
    for x in h.readlines() :
        (n,t) = x.strip().lower().split("|")
        external[n] = t # add drug into the dicitonary with the corresponding type

# obtain the list of english stopword
stop_words = stopwords.words('english') 

# build regular expression patterns for lower and upper chars
lower = re.compile(r'.*[a-z]+')
upper = re.compile(r'.*[A-Z]+')

# feature extractor function
def extract_features(tokens) :

   # for each token, generate list of features and add it to the result
   result = []
   for k in range(0,len(tokens)):
      tokenFeatures = []; # features of the current token
      t = tokens[k][0]

      # external-knowledge based feature
      if t.lower() in external:
         tokenFeatures.append("external="+external[t.lower()])

      tokenFeatures.append("form="+t)

      # lower_case form 
      tokenFeatures.append("lower_form="+ t.lower())

      # title_form
      tokenFeatures.append("title_form="+t.title())

      # camel-case
      tokenFeatures.append("camelCase_form="+camel_case(t))

      # capitalized
      tokenFeatures.append("capitalized_form="+t.capitalize())
      
      #stopword 
      if t.lower() in stop_words:   
         tokenFeatures.append("is_stopword")

      # is_alpha
      if t.isalpha():
         tokenFeatures.append("is_alpha="+t)

      # suffixes and prefixes of the current token
      tokenFeatures.append("suf3="+t[-3:])
      tokenFeatures.append("pref3="+t[:3])
      tokenFeatures.append("suf2="+t[-2:])
      tokenFeatures.append("pref2="+t[:2])
      tokenFeatures.append("suf4="+t[-4:])
      tokenFeatures.append("pref4="+t[:4]) 
      tokenFeatures.append("suf5="+t[:-5])
      tokenFeatures.append("pref5="+t[:5])

      # upper
      if t.isupper():
         #tokenFeatures.append("isUpper="+t)
         tokenFeatures.append("isUpper=UP")

      # dash
      if '-' in t:
         tokenFeatures.append("contains_dash")

      # contains any digit (taken from the baseline rules)
      if any(char.isdigit() for char in t):
         tokenFeatures.append("text=withDigit")

      # is upper and lower current word
      if lower.match(t) and upper.match(t):
         tokenFeatures.append("lowerAndUpper")

      # contains only digits
      if all(char.isdigit() for char in t):
         tokenFeatures.append("text=onlyDigits")

      # length
      tokenFeatures.append("length=%s" %len(t) )


      # features for the previous token 
      if k>0 :
         tPrev = tokens[k-1][0]

         # external knowledge based feature
         if tPrev.lower() in external:
            tokenFeatures.append("externalPrev="+external[tPrev.lower()]) 

         # form
         tokenFeatures.append("formPrev="+tPrev)
         
         #lower form
         tokenFeatures.append("lower_formPrev="+tPrev.lower())

         # title_form
         tokenFeatures.append("title_formPrev="+tPrev.title())

         # is_alpha
         if tPrev.isalpha():
            tokenFeatures.append("is_alphaPrev="+tPrev)

         #stopword
         if tPrev.lower() in stop_words:   
         #  tokenFeatures.append("is_stopwordPrev="+tPrev.lower())
            tokenFeatures.append("is_stopwordPrev")

         # pref and suf  
         tokenFeatures.append("suf3Prev="+tPrev[-3:])
         tokenFeatures.append("pref3Prev="+tPrev[:3])
         tokenFeatures.append("suf2Prev="+tPrev[-2:])
         tokenFeatures.append("pref2Prev="+tPrev[:2])
         tokenFeatures.append("suf4Prev="+tPrev[-4:])
         tokenFeatures.append("pref4Prev="+tPrev[:4])
         tokenFeatures.append("suf5Prev="+tPrev[-5:])
         tokenFeatures.append("pref5Prev="+tPrev[:5])

         # length 
         tokenFeatures.append("lengthPrev=%s" %len(tPrev) )

      else :
         tokenFeatures.append("BoS")


      # features for the token 2 positions before from the current one
      if k > 1:
         tPrev2 = tokens[k-2][0]

         # external knowledge based features
         if tPrev2.lower() in external:
            tokenFeatures.append("externalPrev2="+external[tPrev2.lower()]) 

         tokenFeatures.append("formPrev2="+tPrev2)
         
         #lower form 
         tokenFeatures.append("lower_formPrev2="+tPrev2.lower())

         # title_form
         tokenFeatures.append("title_formPrev2="+tPrev2.title())

         # pref and suf 
         tokenFeatures.append("suf3Prev2="+tPrev2[-3:])
         tokenFeatures.append("pref3Prev2="+tPrev2[:3])
         tokenFeatures.append("suf2Prev2="+tPrev2[-2:])
         tokenFeatures.append("pref2Prev2="+tPrev2[:2])
         tokenFeatures.append("suf4Prev2="+tPrev2[-4:])
         tokenFeatures.append("pref4Prev2="+tPrev2[:4])
         tokenFeatures.append("suf5Prev2="+tPrev2[-5:])
         tokenFeatures.append("pref5Prev2="+tPrev2[:5])

         #length
         tokenFeatures.append("lengthPrev2=%s" %len(tPrev2) )
      

      # # features for the token 1 position ahead from the current one
      if k<len(tokens)-1 :
         tNext = tokens[k+1][0]

         # external knowledge based feature
         if tNext.lower() in external:
            tokenFeatures.append("externalNext="+external[tNext.lower()]) 

         tokenFeatures.append("formNext="+tNext)

         #lower form 
         tokenFeatures.append("lower_formNext="+tNext.lower())

         # title_form
         tokenFeatures.append("title_formNext="+tNext.title())

         #stopword
         if tNext.lower() in stop_words:   
            tokenFeatures.append("is_stopwordNext")

         # is_alpha
         if tNext.isalpha():
            tokenFeatures.append("is_alphaNext="+tNext)

         # pref and suf
         tokenFeatures.append("suf3Next="+tNext[-3:])
         tokenFeatures.append("pref3Next="+tNext[:3])
         tokenFeatures.append("suf2Next="+tNext[-2:])
         tokenFeatures.append("pref2Next="+tNext[:2])
         tokenFeatures.append("suf4Next="+tNext[-4:])
         tokenFeatures.append("pref4Next="+tNext[:4])
         tokenFeatures.append("suf5Next="+tNext[-5:])
         tokenFeatures.append("pref5Next="+tNext[:5])

         # length of the following token
         tokenFeatures.append("lengthNext=%s" %len(tNext) )
      else:
         tokenFeatures.append("EoS")
      

      # features for the token 2 positions ahead from the current one
      if k<len(tokens) - 2:
         tNext2 = tokens[k+2][0]

         # external knowledge based features
         if tNext2.lower() in external:
            tokenFeatures.append("externalNext2="+external[tNext2.lower()])

         tokenFeatures.append("formNext2="+tNext2)

         #lower form 
         tokenFeatures.append("lower_formNext2="+tNext2.lower())

         # title_form
         tokenFeatures.append("title_formNext2="+tNext2.title())

         #length
         tokenFeatures.append("lengthNext2=%s" %len(tNext2) )
   
    
      result.append(tokenFeatures)
    
   return result


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir, and writes
## -- them in the output format requested by the evalution programs.
## --


# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :
   
   # parse XML file, obtaining a DOM tree
   tree = parse(datadir+"/"+f)
   
   # process each sentence in the file
   sentences = tree.getElementsByTagName("sentence")
   for s in sentences :
      sid = s.attributes["id"].value   # get sentence id
      spans = []
      stext = s.attributes["text"].value   # get sentence text
      entities = s.getElementsByTagName("entity")
      for e in entities :
         # for discontinuous entities, we only get the first span
         # (will not work, but there are few of them)
         (start,end) = e.attributes["charOffset"].value.split(";")[0].split("-")
         typ =  e.attributes["type"].value
         spans.append((int(start),int(end),typ))
         

      # convert the sentence to a list of tokens
      tokens = tokenize(stext)
      # extract sentence features
      features = extract_features(tokens)

      # print features in format expected by crfsuite trainer
      for i in range (0,len(tokens)) :
         # see if the token is part of an entity
         tag = get_tag(tokens[i], spans) 
         print (sid, tokens[i][0], tokens[i][1], tokens[i][2], tag, "\t".join(features[i]), sep='\t')

      # blank line to separate sentences
      print()