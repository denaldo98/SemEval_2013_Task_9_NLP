#! /usr/bin/python3

import sys
import re
from os import listdir

from xml.dom.minidom import parse

from deptree import *

# this is for exploring e.g. how many times do I have this patterns , etc., etc., 

# -----------------
# check pattern:  LCS is a verb, one entity is under its "nsubj" and the other under its "obj"
def check_pattern_LCS_svo(tree,entities,e1,e2):

   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1,tkE2)

      if tree.get_tag(lcs)[0:2] == "VB" : 
         path1 = tree.get_up_path(tkE1,lcs)
         path2 = tree.get_up_path(tkE2,lcs)
         func1 = tree.get_rel(path1[-1]) if path1 else None
         func2 = tree.get_rel(path2[-1]) if path2 else None
   
         if (func1=='nsubj' and func2=='obj') or (func1=='obj' and func2=='nsubj') :
            return [tree.get_lemma(lcs)+'_'+tree.get_tag(lcs)[0:2]] # instead of checking which is the verb, just returns the list of verbs in between to know which verbs to use
   
   return None

# -----------------
# check pattern:  LCS is a verb, one entity is under its "nsubj" and the other under its "obj"
def check_pattern_wib(tree,entities,e1,e2):

   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   if tkE1 is not None and tkE2 is not None:
      # get actual start/end of both entities
      l1,r1 = entities[e1]['start'],entities[e1]['end']
      l2,r2 = entities[e2]['start'],entities[e2]['end']
      
      p = []
      for t in range(tkE1+1,tkE2) :
         # get token span
         l,r = tree.get_offset_span(t)
         # if the token is (syntactically) in between both entities
         if r1 < l and r < l2:
            p.append(tree.get_lemma(t))
      if p :
         return p # return the list of words in between

   return None

# -----------------
# check pattern:  LCS is a verb with a 'should' child
def check_pattern_should_advise(tree, entities, e1, e2):
   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1,tkE2)

      if tree.get_tag(lcs)[0:2] == "VB":
         for child in tree.get_children(lcs):
            if tree.get_lemma(child) == 'should':
               return [tree.get_lemma(lcs)+'_'+tree.get_tag(lcs)[0:2]]
   
   return None

# -----------------
# check pattern:  the 2 entities are the same
def check_pattern_same_entities(tree, entities, e1, e2):
   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   if tkE1 is not None and tkE2 is not None:
      if tree.get_lemma(tkE1) == tree.get_lemma(tkE2):
         return [tree.get_lemma(tkE1)+'_'+tree.get_lemma(tkE2)] 
      
   return None

def check_e1_under_e2(tree, entities, e1, e2):
   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   if tkE1 is not None and tkE2 is not None:
      if tkE2 == tree.get_parent(tkE1):
         return [tree.get_lemma(tkE1)+'_'+tree.get_lemma(tkE2)] 
      
   return None

def check_same_parent_verb(tree, entities, e1, e2):
   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   if tkE1 is not None and tkE2 is not None:
      p1 = tree.get_parent(tkE1)
      p2 = tree.get_parent(tkE2)
      if p1 == p2 and tree.get_tag(p1)[0:2] not in ['VB', 'NN']:
         return [tree.get_lemma(tkE1)+'_'+tree.get_lemma(tkE2)] 

def check_parent_e1(tree, entities, e1, e2):
   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])
   if tkE1 is not None and tkE2 is not None:
      p1 = tree.get_parent(tkE1)
      if p1 is not None:
         lemma = tree.get_lemma(p1).lower()
         return [lemma]

def check_parent_e2(tree, entities, e1, e2):
   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])
   if tkE1 is not None and tkE2 is not None:
      p2 = tree.get_parent(tkE2)
      if p2 is not None:
         lemma = tree.get_lemma(p2).lower()
         return [lemma] 




   
## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir
## --


# directory with files to process
datadir = sys.argv[1]

countMT = {"mechanism":0, "effect":0, "int":0, "advise":0, "null":0}
countPT = {}
countP = {}
countM = 0

# process each file in directory
for f in listdir(datadir) :

   # parse XML file, obtaining a DOM tree
   tree = parse(datadir+"/"+f)

   # process each sentence in the file
   sentences = tree.getElementsByTagName("sentence")
   for s in sentences :
      sid = s.attributes["id"].value   # get sentence id
      stext = s.attributes["text"].value   # get sentence text
      
      analysis = deptree(stext)
        
      # load sentence entities
      entities = {}
      ents = s.getElementsByTagName("entity")
      for e in ents :
         id = e.attributes["id"].value
         offs = e.attributes["charOffset"].value.split("-")           
         entities[id] = {'start': int(offs[0]),
                         'end': int(offs[-1]),
                         'type': e.attributes["type"].value,
                         'text': e.attributes["text"].value}

      # for each pair in the sentence, decide whether it is DDI and its type

      pairs = s.getElementsByTagName("pair")
      for p in pairs:
         id_e1 = p.attributes["e1"].value
         id_e2 = p.attributes["e2"].value

         ddi = p.attributes["ddi"].value
         typ = p.attributes["type"].value if ddi=="true" else "null"

         ####################################################
         # check ONE pattern and collect statistics about it
         #match = check_pattern_LCS_svo(analysis, entities, id_e1, id_e2)

         # add pattern functions to explore other possibilities. Run the program
         # with ONE pattern active at a time.
         
         #match = check_pattern_wib(analysis, entities, id_e1, id_e2)
         #match = check_my_other_pattern(analysis, entities, id_e1, id_e2)
         #match = check_pattern_should_advise(analysis, entities, id_e1, id_e2)
         #match = check_pattern_same_entities(analysis, entities, id_e1, id_e2)
         #match = check_e1_under_e2(analysis, entities, id_e1, id_e2)
         #match = check_same_parent_verb(analysis, entities, id_e1, id_e2)
         #match = check_parent_e2(analysis, entities, id_e1, id_e2)
         match = check_parent_e1(analysis, entities, id_e1, id_e2)
         ####################################################
         
         if match is not None :            
            print('-------------')
            print('sentence:',stext)
            print('entities:',entities[id_e1]['text'],"/",entities[id_e2]['text'])
            print('ddi:',typ)
            # uncomment to see the tree for this sentence
            #analysis.print()
            
            for m in match: # for all the matches in will count how many times this thing happens for each of the classes, eg. ....
               print('>>> match:',m)            

               countM += 1     # total num of matches 
               countMT[typ] += 1  # total num of matches per ddi type
            
               # count match instantiations
               if m in countP: countP[m] +=1
               else: countP[m] = 1

               # count match instantiation + ddi type coocurrences
               key = m+"#"+typ
               if key in countPT: countPT[key] += 1
               else: countPT[key] = 1


print("----------------------")
if countM == 0 :
   print('no matches found')

else:
   print(f"{countM} matches found")
   print("----------------------")
   for t in countMT :
      print(f"P({t}|ANY) = {countMT[t]}/{countM} = {countMT[t]/countM}")
   print("----------------------")
   for m in countP:
      for t in countMT:
         k = m+"#"+t 
         if k in countPT:
            print(f"P({t}|{m}) = {countPT[k]}/{countP[m]} = {countPT[k]/countP[m]}")
