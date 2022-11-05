#! /usr/bin/python3

import sys
from os import listdir
from xml.dom.minidom import parse

from deptree import *
import patterns

# clue verbs of each interaction
effect_list = ['diminish','augment','exhibit','experience','counteract','potentiate','enhance','reduce','antagonize', 'include', 'block']
mechanism_list = ['impair','inhibit','displace','accelerate','bind','induce','decrease','elevate','delay', 'increase', 'indicate', 'produce']
advise_list = ['exceed']
int_list = ['suggest']
clue_verbs = effect_list+mechanism_list+advise_list+int_list

## ------------------- 
## -- Convert a pair of drugs and their context in a feature vector

def extract_features(tree, entities, e1, e2) :
   feats = set()

   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   if tkE1 is not None and tkE2 is not None:

      # num of tokens in between
      feats.add("ntokens_in_bt="+str(tkE2 - tkE1))

      # features for tkE1
      feats.add('tkE1_word='+tree.get_word(tkE1))
      feats.add('tkE1_lemma='+tree.get_lemma(tkE1).lower())
      feats.add('tkE1_tag='+tree.get_tag(tkE1))
      feats.add('tkE1_word_lenght'+str(len(tree.get_word(tkE1))))
      feats.add('tkE1_lemma_lenght'+str(len(tree.get_lemma(tkE1))))

      # features for tkE2
      feats.add('tkE2_word='+tree.get_word(tkE2))
      feats.add('tkE2_lemma='+tree.get_lemma(tkE2).lower())
      feats.add('tkE2_tag='+tree.get_tag(tkE2))
      feats.add('tkE2_word_lenght'+str(len(tree.get_word(tkE2))))
      feats.add('tkE2_lemma_lenght'+str(len(tree.get_lemma(tkE2))))

      # features for tokens in between E1 and E2
      for tk in range(tkE1+1, tkE2) :
         if not tree.is_stopword(tk):
            word  = tree.get_word(tk)
            lemma = tree.get_lemma(tk).lower()
            tag = tree.get_tag(tk)
            rel = tree.get_rel(tk)
            feats.add("lib=" + lemma)
            feats.add("wib=" + word)
            feats.add("rib=" + rel) 
            feats.add("tib=" + tag) 
            feats.add("lpib=" + lemma + "_" + tag)

            # check clue verb in between
            if tag == "VB" and lemma in clue_verbs:
               feats.add("clue_verb_ib="+lemma)

            # entity in between tkE1 and tkE2
            if tree.is_entity(tk, entities) :
               feats.add("eib")

      # features for tokens before tkE1
      for tk in range(tkE1):
         if not tree.is_stopword(tk):
            word  = tree.get_word(tk)
            lemma = tree.get_lemma(tk).lower()
            tag = tree.get_tag(tk)
            feats.add("l_before=" + lemma)
            feats.add("w_before=" + word)
            feats.add("lp_before=" + lemma + "_" + tag)

            # clue verb before tkE1
            if tag == "VB" and lemma in clue_verbs:
               feats.add("clue_verb_before="+lemma)

            # entity before tkE1
            if tree.is_entity(tk, entities):
               feats.add("ebf")

      # features for tokens after tkE2
      for tk in range(tkE2, tree.get_n_nodes()):
         if not tree.is_stopword(tk):
            word  = tree.get_word(tk)
            lemma = tree.get_lemma(tk).lower()
            tag = tree.get_tag(tk)
            feats.add("l_after=" + lemma)
            feats.add("w_after=" + word)
            feats.add("lp_after=" + lemma + "_" + tag)

            # clue verb after tkE2           
            if tag == "VB" and lemma in clue_verbs:
               feats.add("clue_verb_after="+lemma)

            # entity after E2
            if tree.is_entity(tk, entities):
               feats.add("eaf")

      # features about the LCS
      lcs = tree.get_LCS(tkE1,tkE2)

      word  = tree.get_word(lcs)
      lemma = tree.get_lemma(lcs).lower()
      tag = tree.get_tag(lcs)
      rel = tree.get_rel(lcs)
      feats.add("LCS_w=" + word)
      feats.add("LCS_l=" + lemma)
      feats.add("LCS_tag=" + tag)
      feats.add("LCS_rel=" + rel)
      feats.add("LCS_ l_t=" + lemma + "_" + tag)

      # LCS is entity
      if tree.is_entity(lcs, entities):
         feats.add("lcs_entity")
      
      # LCS is ROOT
      if lcs == "ROOT":
         feats.add("lcs_root")

      # features for both entities
      feats.add("lemma_pair="+"_".join(sorted([tree.get_lemma(tkE1).lower(),tree.get_lemma(tkE2).lower()])))
      feats.add("tag_pair="+"_".join(sorted([tree.get_tag(tkE1),tree.get_tag(tkE2)])))
      feats.add("word_pair="+"_".join(sorted([tree.get_word(tkE1),tree.get_word(tkE2)])))

      # features about PATHS in the tree
      path1 = tree.get_up_path(tkE1,lcs)
      str_path1 = "<".join([tree.get_lemma(x).lower()+"_"+tree.get_rel(x) for x in path1])
      # path containing only tags
      str_path1_tags = "<".join([tree.get_tag(x) for x in path1])
      feats.add("path1="+str_path1)
      feats.add("path1_tags="+str_path1_tags)

      path2 = tree.get_down_path(lcs,tkE2)
      str_path2 = ">".join([tree.get_lemma(x).lower()+"_"+tree.get_rel(x) for x in path2])
      str_path2_tags = ">".join([tree.get_tag(x) for x in path2])
      feats.add("path2="+str_path2)
      feats.add("pat2_tags="+str_path2_tags)

      path = str_path1+"<"+tree.get_lemma(lcs)+"_"+tree.get_rel(lcs)+">"+str_path2      
      feats.add("path="+path)
      path_tags = str_path1_tags+"<"+tree.get_tag(lcs)+">"+str_path2_tags
      feats.add("path_tags="+path_tags) 
      
      # entity inside path
      for tk in path1 + path2:
         if tree.is_entity(tk, entities):
            feats.add("entity_in_path="+tree.get_lemma(tk).lower())

      #condensed path (seen in class)
      if len(path1) > 0 and len(path2) > 0:
         condensed_path = tree.get_rel(path1[-1])+"*<"
         condensed_path += tree.get_lemma(lcs).lower()+">*"+tree.get_rel(path2[0])
         feats.add("condensed_path="+condensed_path)

      # path wiht entities inside
      path_Entity = ""
      for tk in path1:
         path_Entity += ("Entity/"+tree.get_rel(tk) if tree.is_entity(tk, entities) else tree.get_rel(tk))+"<"
      path_Entity += tree.get_rel(lcs)
      for tk in path2:
         path_Entity+= ">"+("Entity/"+tree.get_rel(tk) if tree.is_entity(tk, entities) else tree.get_rel(tk))
      feats.add("pathEntity="+path_Entity)

      # lengths of the paths
      feats.add("path1_len="+str(len(path1)))
      feats.add("path2_len="+str(len(path2)))
      feats.add("tot_len="+str(len(path1)+len(path2)+(1 if lcs != "ROOT" else 0)))

      # features about parent entities
      p1 = tree.get_parent(tkE1)
      p2 = tree.get_parent(tkE2)

      # parent of E1 
      if p1 is not None:
         lemma = tree.get_lemma(p1).lower()
         tag = tree.get_tag(p1)
         feats.add("lp1=" + lemma)
         feats.add("tp1=" + tag) 
      
      # parent of E2
      if p2 is not None:
         lemma = tree.get_lemma(p2).lower()
         tag = tree.get_tag(p2)
         feats.add("lp2=" + lemma)
         feats.add("tp2=" + tag) 

      # same entities in the pair
      if tree.get_lemma(tkE1) == tree.get_lemma(tkE2):
         feats.add("same_lemma")

      # e1 under e2
      if tkE2 == tree.get_parent(tkE1):
         feats.add("e1_under_e2")
      
      # e2 under e1
      if tkE1 == tree.get_parent(tkE2):
         feats.add("e2_under_e1")

      # same parent
      if p1 == p2 and (p1 is not None):
         tag = tree.get_tag(p1)
         feats.add("same_parent_tag=" + tag) 

      # LCS is a verb with a 'should' child
      should_advise_rule = patterns.check_should_advise(tree, tkE1, tkE2)
      if should_advise_rule:
         feats.add("should_advise_rule")
      

   return feats


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  extract_features targetdir
## --
## -- Extracts feature vectors for DD interaction pairs from all XML files in target-dir
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
        stext = s.attributes["text"].value   # get sentence text
        # load sentence entities
        entities = {}
        ents = s.getElementsByTagName("entity")
        for e in ents :
           id = e.attributes["id"].value
           offs = e.attributes["charOffset"].value.split("-")
           type = e.attributes["type"].value 
           entities[id] = {'start': int(offs[0]), 'end': int(offs[-1]), 'type':type}       
           #entities[id] = {'start': int(offs[0]), 'end': int(offs[-1])}

        # there are no entity pairs, skip sentence
        if len(entities) <= 1 : continue

        # analyze sentence
        analysis = deptree(stext)

        # for each pair in the sentence, decide whether it is DDI and its type
        pairs = s.getElementsByTagName("pair")
        for p in pairs:
            # ground truth
            ddi = p.attributes["ddi"].value
            if (ddi=="true") : dditype = p.attributes["type"].value
            else : dditype = "null"
            # target entities
            id_e1 = p.attributes["e1"].value
            id_e2 = p.attributes["e2"].value
            # feature extraction

            feats = extract_features(analysis,entities,id_e1,id_e2) 
            # resulting vector
            print(sid, id_e1, id_e2, dditype, "\t".join(feats), sep="\t")

