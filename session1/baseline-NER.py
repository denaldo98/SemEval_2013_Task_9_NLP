#! /usr/bin/python3


import sys
from os import listdir,system
import re
from tokenize import group
import nltk
nltk.download('punkt')

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

import evaluator as evaluator

## dictionary containing information from external knowledge resources
## WARNING: You may need to adjust the path to the resource files
external = {}

path = "TaskData/resources/HSDB.txt"
with open(path, encoding="utf8") as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"
with open("TaskData/resources/DrugBank.txt", encoding="utf8") as h :
    for x in h.readlines() :
        (n,t) = x.strip().lower().split("|")
        external[n] = t

        
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    for t in word_tokenize(txt):
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)
    return tks

## -----------------------------------------------
## -- check if a token is a drug part, and of which type

# suffixes for drug
#suffixes = ('inine', 'lline', 'ucose','ridol', 'tocin', 'ipine', 'brate', 'limus', 'navir', 'illin','necid', 'ostat', 'thron', 'coxib', 'uride', 'ytoin')

# suffixes for group
group_suffixes = ('tics', 'lant', 'ants', 'ones', 'ists', 'alis', 'iral','ioid')

# suffixes for drug_n
drug_n_suff = ('hydro', 'methyl', 'Nep')

def classify_token(txt):
    
    # check presence in external knowledge resources
    if txt.lower() in external : return external[txt.lower()]
    
    # group rules
    elif txt.lower().endswith(group_suffixes): return "group"
    elif len(txt) > 12 and txt[-1:] == 's': return "group"  

    # drug_n rules
    elif any(char.isdigit() for char in txt) and len(txt) > 5 and '-' in txt: return "drug_n"
    elif any(suff in txt for suff in drug_n_suff): return "drug_n" 
    elif '[' in txt and len(txt) > 2: return 'drug_n'
    else : return "NONE"

   
## --------- Entity extractor ----------- 
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"

def extract_entities(stext) :
    
    # tokenize text
    tokens = tokenize(stext)    
    result = []

    # previously classified drug: we need it to manage multi-token drug names
    previous_drug = ""

    # classify each token and decide whether it is an entity.
    for (token_txt, token_start, token_end)  in tokens:
        # classify current token
        drug_type = classify_token(token_txt)

        # create and add the entity to the result list
        if drug_type in ['drug', 'drug_n', 'brand']:

            # save current recognized drug to check it at the next iteration
            previous_drug = str(token_txt)+" "+str(token_start)+" "+str(drug_type)
            # create entity dictionary
            e = { "offset" : str(token_start)+"-"+str(token_end),
                  "text" : stext[token_start:token_end+1],
                  "type" : drug_type
                 }
            result.append(e) # append entity to the result list
        
        # case of 'group' current drug type: check previously recognized drug
        elif drug_type == 'group': 
            if previous_drug != "": # check if the previous token is a drug of type 'group'
                prev_drug_info = previous_drug.split(" ") # contains the text, offset and type of the previously classified drug
                if len(result) > 0 and prev_drug_info[2] == "group":
                    result.pop() # multi-token drug of type 'group' recognized: pop the previously inserted entity to add the new multi-token one
                    e = { "offset" : str(prev_drug_info[1])+"-"+str(token_end), # initial offset is the one of the previous recognized drug
                          "text" : stext[int(prev_drug_info[1]):token_end+1], # text composed of multiple tokens
                          "type" : 'group' 
                        } 
            
            # previous token not a recognized drug: just add the current entity as type 'group'
            else: 
                e = { "offset" : str(token_start)+"-"+str(token_end),
                  "text" : stext[token_start:token_end+1],
                  "type" : 'group'
                 }
                result.append(e)
            previous_drug = str(token_txt)+" "+str(token_start)+" "+str(drug_type)

        # current token is not a drug
        else:
            previous_drug = ""

    return result
      
## --------- main function ----------- 

def nerc(datadir, outfile) :
   
    # open file to write results
    outf = open(outfile, 'w')

    # process each file in input directory
    for f in listdir(datadir) :
      
        # parse XML file, obtaining a DOM tree
        tree = parse(datadir+"/"+f)
      
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value   # get sentence id
            stext = s.attributes["text"].value   # get sentence text
            
            # extract entities in text
            entities = extract_entities(stext)
         
            # print sentence entities in format requested for evaluation
            for e in entities :
                print(sid,
                      e["offset"],
                      e["text"],
                      e["type"],
                      sep = "|",
                      file=outf)
            
    outf.close()


   
## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir
## --

# directory with files to process
datadir = sys.argv[1]
outfile = sys.argv[2]

nerc(datadir,outfile)

evaluator.evaluate("NER", datadir, outfile)

