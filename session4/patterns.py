## ------------------- 
## -- check pattern:  LCS is a verb, one entity is under its "nsubj" and the other under its "obj"      

def check_LCS_svo(tree,tkE1,tkE2):

   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1,tkE2) # get the lowest common subsumer

      if tree.get_tag(lcs)[0:2] == "VB" :  #if it is a verb     
         path1 = tree.get_up_path(tkE1,lcs) # get the path from the 1st entity to the LCS
         path2 = tree.get_up_path(tkE2,lcs) # get the path from the 2nd entity to the LCS
         func1 = tree.get_rel(path1[-1]) if path1 else None # get the last element/word of the path (the one immediately below the LCS)
         func2 = tree.get_rel(path2[-1]) if path2 else None
         
         if (func1=='nsubj' and func2=='obj') or (func1=='obj' and func2=='nsubj') : # if one of them is the subject and the other an object
            lemma = tree.get_lemma(lcs).lower() # I get the lemma of the LCS, i-.e the infinitive of the verb
            if lemma in ['diminish','augment','exhibit','experience','counteract','potentiate','enhance','reduce','antagonize', 'include', 'block'] :
               return 'effect' # if the lemma is one of the above, the relationship is of type effect
            if lemma in ['impair','inhibit','displace','accelerate','bind','induce','decrease','elevate','delay', 'increase', 'indicate', 'produce'] :
               return 'mechanism'
            if lemma in ['exceed'] : # 'mantain', 'useda', 'extend', 'require'
               return 'advise'
            if lemma in ['suggest'] :
               return 'int'
         
   return None

## ------------------- 
## -- check pattern:  A word in between both entities belongs to certain list

def check_wib(tree,tkE1,tkE2,entities,e1,e2):

   if tkE1 is not None and tkE2 is not None:
      # get actual start/end of both entities
      l1,r1 = entities[e1]['start'],entities[e1]['end']
      l2,r2 = entities[e2]['start'],entities[e2]['end']
      
      p = []
      for t in range(tkE1+1,tkE2) : # for all the tokens in between these 2 entities
         # get token span
         l,r = tree.get_offset_span(t)
         # if the token is in between both entities
         if r1 < l and r < l2:
            lemma = tree.get_lemma(t).lower()
            if lemma in ['phosphorylation', 'enhance', 'locomotor', 'action', 'response', 'oxidative', 'stress', 'e', 'ig', '4th', 'protection', 'tbars', 'cerebral', 'radical', 'damage', 'peroxidation', 'ie', 'man', 'bleeding', 'odds', 'retinal', 'transduction', 'counteract', 'equally', 'antagonize', 'stimulate', 'proliferation', 'epithelium', 'transferrin', 'mitogenic', 'regulate', 'prostate', 'modification', 'secondary', 'adrenocortical', 'augment', 'alcohol', 
'neuron', 'central', 's.', 'c.', 'mumol', 'liter', 'rarely', 'ventricular', 'fibrillation', 'asparaginase', 'antineoplastic', 'weakness', 'hyperreflexia', 'incoordination', 'acetyltransferase', 'consequence', 'Abciximab', 'photosensitivity', 'actinic', 'keratose', 'aggregation', 'cilostazol', 'exacerbate', 'prothrom', 'bin', 'tendency', 'hypokalemic', 'antiplatelet', 'exaggerate', 'syndrome', 'AKINETON', 'transdermal', 'nervous', 'mefloquine', 'Parkinsons', 'antagonistic', 'antiparkinsonian', 'trihexyphenidyl', 'related', 'oxygen', 'nimbex', 'sleeping', 'accentuate', 'glaucoma', 'serotoninergic', 'migraine', 'Imitrex', 'bacteriostatic', 'hyperuricemic', 'hypoparathyroid', 'sodation', 'halogenate', 'hydrocarbon', 'autonomic', 'irritability', 'arrhythmia', 'NUROMAX', 'lengthen', 'occurrence', 'ototoxic', 'Injection', 'timolol', 'rebound', 'antimuscarinic', 'weaken', 'metaraminol', 'abciximab', 'GP', 'iib', 'iiia', 'tabloid']:
               return 'effect'
            if lemma in ['acute', 'biotransformation', 'statistically', 'Lomefloxacin', 'react', 'faster', '31', 'induction', 'due', 'presumably', 'accelerate', 'pancreatin', 'cyp', 'Cmin', 'medicinal', 'modest', 'displace', 'Acetazolamide', 'Acetaminophen', 'q12h', '1a2', 'malabsorption', 'ascorbic', 'fruit', 'phosphate', 'ionized', 'species', 'ed50', 'John', 'p450iiia4', 'elc', 'gefitinib', 'carbonate', 'plasmaconcentration', 'triazolo', 'ingest', 'where', 'determinant', 'indigestion', 'remedy', 'intense', 'respiratory', 'sulfamethizole', 'sulphasalazine', 'tpmt']:
               return 'mechanism'
            if lemma in ['index', 'SSRI', 'pth', 'methysergide', 'Ophthalmic', 'Solution', 'pulse', 'myocardial', 'SUBOXONE', 'isoenzyme', 'management', 'nephrotoxic', 'withdraw', 'cautiously', 'exceed', 'predominantly', 'narrow', 'window', 'supraventricular', 'terbinafine', 'tell', 'doctor', 'buprenorphine', 'pure', 'methylergonovine', 'antimycotic', 'adjunctive', '533', '133', 'isrecommend', 'INVEGA']:
               return 'advise'
            if lemma in ['interact', 'Diuretics', 'Tylenol', 'cyp2b6', 'MIVACRON', 'incompatible', 'thiamine', 'Loop']:
               return 'int'

   return None

## ------------------- 
# check pattern:  LCS is a verb with a 'should' child

def check_should_advise(tree, tkE1, tkE2):

    if tkE1 is not None and tkE2 is not None:
        lcs = tree.get_LCS(tkE1, tkE2)

        if tree.get_tag(lcs)[0:2] == "VB":
            for child in tree.get_children(lcs):
                if tree.get_lemma(child) == 'should':
                    return 'advise'
    return None

## ------------------- 
# check pattern:  both entities in the pair are the same, in that case return 'null'

def check_pattern_same_entities(tree, tkE1, tkE2):

   if tkE1 is not None and tkE2 is not None:
      if tree.get_lemma(tkE1) == tree.get_lemma(tkE2):
         return 'null'
   return None


def check_group_after_brand(entities, e1, e2):

    if entities[e1]['type'] == 'brand' and entities[e2]['type'] == 'group':
        return 'effect'


def check_e1_under_e2(tree, tkE1, tkE2):

   if tkE1 is not None and tkE2 is not None:
      if tkE2 == tree.get_parent(tkE1):
         return 'null'
   return None

def check_e2_under_e1(tree, tkE1, tkE2):

   if tkE1 is not None and tkE2 is not None:
      if tkE1 == tree.get_parent(tkE2):
         return 'null'
   return None



def check_same_parent(tree, tkE1, tkE2):

   if tkE1 is not None and tkE2 is not None:
      p1 = tree.get_parent(tkE1)
      p2 = tree.get_parent(tkE2)

      if p1 == p2 and (p1 is not None): # same parent
         if tree.get_tag(p1)[0:2] not in ['NN', 'VB']: # parent not a verb or noun
            return 'null'
         if tree.get_tag(p1)[0:2] == 'VB':
            return 'advise'
   return None
            
# entity 1 under list of possible lemmaa
def check_parent_e1(tree, tkE1, tkE2):
   if tkE1 is not None and tkE2 is not None:
      p1 = tree.get_parent(tkE1)
      if p1 is not None:
         lemma = tree.get_lemma(p1).lower()
         if lemma in ['user', 'enhance', 'attenuate', 'efficacy', 'pretreatment', 'action', 'time', 'ethynyl', 'response', 'mediate', 'block', 'dexamethasone', 'glucocorticoid', 'min', 'augment', 'experience', 'prolong', 'vasopressor',
'diminish', 'chloramphenicol', 'exaggerate', 'syndrome', 'butalbital', 'quinolone', 'counteract', 'butyrophenones', 'cyclopropane', 'impair', 'exacerbate', 'epinephrine', 'only', 'stavudine', 'resistance', 'phosphorylation', 'anticoagulants', 'capable', 'purinethol']:
            return 'effect'
         if lemma in ['presence', 'trovafloxacin', 'moxifloxacin', 'react', 'modify', 'absorption', 'calcium', 'expect', 'exist', 'know', 'q12h', 'compete', 'equivalent', 'videx', 'course']:
            return 'mechanism'
         if lemma in ['b1']:
           return 'int'
         if lemma in ['exert', 'start', 'dihydroergotamine', 'avoid', 'when', 'titrate', 'stop', 'capsules', 'exhibit', 'tell', 'gland', 'beadminister', 'while']:
            return 'advise'
   return None

# entity 2 under list of possible lemmaa
def check_parent_e2(tree, tkE1, tkE2):
   if tkE1 is not None and tkE2 is not None:
      p2 = tree.get_parent(tkE2)
      if p2 is not None:
         lemma = tree.get_lemma(p2).lower()
         if lemma in ['combine', 'effect', 'sensitivity', 'activity', 'enhance', 'initiate', 'add', 'dasatinib', 'action', 'produce', 'egf', 'stimulate', 'antagonize', 'those', 'neurotensin', 'reverse', 'atracurium', 'blockade', 'proleukin', 'alfa', 'coumarin', 'worsen', 'exacerbate', 'include', 'hydrochloride', 'catecholamine', 'cephalosporin', 'anesthesia', 'withdraw', 'tetracycline', 'toxoid', 'imitrex', 'dispersible', 'concomitantly', 'vasodilation', 'exhibit', 'miconazole', 'anticholinergic', 'zyvox', 'starlix', 'pantoprazole', 'piperazine', 'purinethol', 'thioguanine', 'vardenafil', 'sonata']:
            return 'effect'
         if lemma in ['molecule', 'metabolism', 'opiate', 'react', 'whereas', 'media', 'secretion', 'elimination', 'form', 'colestipol', 'displace', 'spray', 'anticipate', 'ergocalcitriol', 'find', 'auc0', 'max', 'mean', 'malabsorption', 'ed50', 'oxyphenbutazone', 'bid', 'vitamin', 'ester']:
            return 'mechanism'
         if lemma in ['solution', 'b1', 'diuretics']:
            return 'int'
         if lemma in ['dosing', 'initiate', 'alosetron', 'any', 'achieve', 'isoenzyme', 'undergo', 'chlorprothixene', 'flecainide', 'sumatriptan', 'avoid', 'start', 'indocin', 'cerezyme', 'naratriptan', 'nevirapine', 'isrecommend', 'vioxx']:
            return 'advise'
   return None
      
