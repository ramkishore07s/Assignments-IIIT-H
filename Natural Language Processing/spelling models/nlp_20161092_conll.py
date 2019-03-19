
# coding: utf-8

# **A Naive-Bayes solution for**
# # `The CoNLL-2014 Shared Task on Grammatical Error Correction`

#  

# In[1]:


import sys
import nltk
import re


# In[2]:


from Assignment1_20161092 import TrigramLanguageModel, train_model, tokeniser, no_files


# In[3]:


## Settings:
WINDOW_SIZE = 1  # Either one or two
USE_POS = True   # This gives the best accuracy on dev set.
REDUCE = False   
ONLY_NN = False  # Unintuitively this gives the worst results on test set. 


# In[4]:


__pos_tag = {}

def get_pos(sentence):
    tags = []
    if USE_POS:
        for word in sentence:
            try: tags.append(__pos_tag[word])
            except:
                pos_tag = nltk.pos_tag([word])[0][1]
                if pos_tag == 'MD' or 'PRP' in pos_tag: __pos_tag[word] = word
                else: __pos_tag[word] = pos_tag
                tags.append(__pos_tag[word])
        return tags
    elif ONLY_NN:
        for word in sentence:
            try: tags.append(__pos_tag[word])
            except:
                pos_tag = nltk.pos_tag([word])[0][1]
                if 'NN' in pos_tag: __pos_tag[word] = pos_tag
                else: __pos_tag[word] = word
                tags.append(__pos_tag[word])
        return tags
    else:
        return sentence


# In[5]:


def get_window(inp, i):
    window = []
    origin = inp[i]
    if WINDOW_SIZE > 1:
        try: window.append(inp[i-2])
        except: pass
    try: window.append(inp[i-1])
    except: pass
    try: window.append(inp[i+1])
    except: pass
    if WINDOW_SIZE > 1:
        try: window.append(inp[i+2])
        except: pass
    
    return window, origin


# In[6]:


f = open('train.txt').read()
lines = f.split('\n\n')
lines = [line.split('\n') for line in lines]
errors = [[( line.index(token), token.split(' ')[-1]) for token in line if len(token.split(' ')) > 1] 
          for line in lines]
data = [[token.split(' ')[0] for token in line] for line in lines]


# ### POS tags

# In[7]:


NOUN = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP']
POSSESIVE = ['PRP$', 'WP$', 'POS']
VERB = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
DT = ['PDT', 'DT']
AD = ['RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS']


# ## POS Model for correct sentences `Gutenberg corpus`

# In[8]:


def pos_tokeniser(text):
    if isinstance(text, str): output = tokeniser(text)
    else: output = [text]
    return [get_pos(line) for line in output]


# In[9]:


# pos_model = TrigramLanguageModel(tokeniser=pos_tokeniser)
# no_files = 10
#
#
# # In[10]:
#
#
# train_model(pos_model, no_files)


# ## Naive Bayes based error model:
# **Naive bayes assumption:** 
# * The error in a sentence does not depend on the entire sentence. i.e. for example: consider the sentence `The dog bark at the car which was moving`. The error in the sentence is the verb `bark`(The correct form is `barks`). I'm assuming that the error depends only on the immediate neighbours of the word, **here:** `dog`, `at`. 
# * So in formal terms, the assumption I'm making is: **The error can be detected only by looking at the immediate neighbours**.
# * However this is not entirely true. Consider: `She just realized that himself`. The correction should be either `She -> He` or `himself -> herself`. The naive bayes assumption made here will fail in those cases.

# In[11]:


# Stores pos for each type of error based on the window size.
# Store counts also.
class ERRORS():
    def __init__(self):
        self.errors = {}
        self.count = {}
        self.total_count = 0
        
    def update(self, err_type, origin, window):
        '''Input is text'''
        
        #filter
        #if err_type == 'Vm' and not get_pos([origin])[0] == 'MD': return
        #if err_type in ['Vt', 'Vform'] and not 'V' in get_pos([origin])[0]: return
        
        if USE_POS:
            window = get_pos(window)
            origin = get_pos([origin])[0]
        if err_type not in self.errors: 
            self.errors[err_type] = {}
            self.count[err_type] = {}
        if origin not in self.errors[err_type]: 
            self.errors[err_type][origin] = [window]
            self.count[err_type][origin] = [1]
        elif window not in self.errors[err_type][origin]: 
            self.errors[err_type][origin].append(window)
            self.count[err_type][origin].append(1)
        else:
            index = self.errors[err_type][origin].index(window)
            self.count[err_type][origin][index] += 1
    
    def __find_pattern(self, err_type, origin, window):
        # update function to return counts also
        try: 
            index = self.errors[err_type][origin].index(window)
            return self.count[err_type][origin][index]
        except Exception as e: 
            return -1
    
    def find_pattern(self, err_type, inp):
        # update function to return counts also
        found_at = []
        counts = []
        for i in range(len(inp)):
            window, origin = get_window(inp, i)
            out = self.__find_pattern(err_type, origin, window)
            if not out == -1: 
                found_at.append(i)
                counts.append(out)
                
        return found_at, counts
    
    def get_error(self, sentence, err_code):
        if USE_POS: sentence = get_pos(sentence)
        found_at, counts = self.find_pattern(err_code, sentence)
        total = float(sum([sum([i for i in self.count[err_code][j]]) for j in self.count[err_code]]))
        return found_at, [i/total for i in counts]


# In[12]:


errModel = ERRORS()


# In[13]:


for errs, line in zip(errors, data):
    for pos, err_type in errs:
        window = []
        if WINDOW_SIZE > 1 and pos > 1: window.append(line[pos - 2])
        if pos > 0: window.append(line[pos - 1])
        if pos < len(line)-1: window.append(line[pos + 1])
        if WINDOW_SIZE > 1 and pos < len(line)-2: window.append(line[pos + 2])
        origin = line[pos]
        errModel.update(err_type, origin, window)


# # ### Verb errors:
# # * `Vt Verb tense` Medical technology during that time **[is → was]** not advanced enough to cure him.
# # * `Vm Verb modal` Although the problem **[would → may]** not be serious, people **[would → might]** still be afraid.
# # * `V0 Missing verb` However, there are also a great number of people **[who → who are]** against this technology.
# # * `Vform Verb form` A study in 2010 **[shown → showed]** that patients recover faster when sur- rounded by family members.
#
# # In[14]:
#
#
# def modal_error(self, sentence):
#     err_code = 'Vm'
#     modal_list = ['will','shall', 'would', 'should', 'ought', 'must','may', 'might', 'can', 'could']
#     return self.get_error(sentence, err_code)
#
#
# # In[15]:
#
#
# def missing_verb(self, sentence):
#     err_code = 'V0'
#     return self.get_error(sentence, err_code)
#
#
# # In[16]:
#
#
# def verb_form(self, sentence):
#     err_code = 'Vform'
#     return self.get_error(sentence, err_code)
#
#
# # In[17]:
#
#
# def verb_tense(self, sentence):
#     err_code = 'Vt'
#     return self.get_error(sentence, err_code)
#
#
# # In[18]:
#
#
# ERRORS.modal_error = modal_error
# ERRORS.missing_verb = missing_verb
# ERRORS.verb_form = verb_form
# ERRORS.verb_tense = verb_tense
#
#
# # ### SVA and Art-Det
# #
# # * `SVA Subject-verb agreement` The benefits of disclosing genetic risk information **[outweighs → out- weigh]** the costs.
# # * `ArtOrDet Article or determiner` It is obvious to see that **[internet → the internet]** saves people time and also connects people globally.
#
# # In[19]:
#
#
# def sva(self, sentence):
#     err_code = 'SVA'
#     return self.get_error(sentence, err_code)
#
#
# # In[20]:
#
#
# def art_det(self, sentence):
#     err_code = 'ArtOrDet'
#     return self.get_error(sentence, err_code)
#
#
# # In[21]:
#
#
# ERRORS.sva = sva
# ERRORS.art_det = art_det
#
#
# # ### Noun errors:
# #
# # * `Nn Noun number` A carrier may consider not having any **[child → children]** after getting married.
# # * `Npos Noun possessive` Someone should tell the **[carriers → carrier’s]** relatives about the genetic problem.
# # * `Pform Pronoun form` A couple should run a few tests to see if **[their → they]** have any genetic diseases beforehand.
# # * `Pref Pronoun reference` It is everyone’s duty to ensure that **[he or she → they]** undergo regular health checks.
#
# # In[22]:
#
#
# def noun_errors(self, sentence):
#     err_code = 'Nn'
#     return self.get_error(sentence, err_code)
#
#
# # In[23]:
#
#
# def npos(self, sentence):
#     err_code = 'Npos'
#     return self.get_error(sentence, err_code)
#
#
# # In[24]:
#
#
# def pform(self, sentence):
#     err_code = 'Pform'
#     return self.get_error(sentence, err_code)
#
#
# # In[25]:
#
#
# def pref(self, sentence):
#     err_code = 'Pref'
#     return self.get_error(sentence, err_code)
#
#
# # In[26]:
#
#
# ERRORS.noun_errors = noun_errors
# ERRORS.npos = npos
# ERRORS.pform = pform
# ERRORS.pref = pref


# In[27]:


def error_prob(self, err_type):
    n = sum([sum([j for j in self.count[err_type][i]]) for i in self.count[err_type]])
    d = sum([sum([sum([j for j in self.count[err_type][i]]) for i in self.count[err_type]]) for err_type in self.count])
    
    return float(n)/float(d)

ERRORS.error_prob = error_prob


# In[28]:


def call(self, sentence):
    errs = ["Nn" ,"Cit" ,"Rloc-" ,"Mec" ,"ArtOrDet" ,"Vform" ,"V0" ,"SVA" ,"Vt" ,"Others" ,"Wform" ,
            "Pform" ,"Wci" ,"Trans" ,"Sfrag" ,"Um" ,"Wtone" , "Prep" ,"Pref" ,"Spar" ,"WOinc" ,
            "Vm" ,"WOadv" ,"Srun" ,"Npos" ,"Ssub" ,"Wa" ,"Smod"]
    candidates = []
    for err in errs:
        indices, values = self.get_error(sentence, err)
        try:
            index = indices[values.index(max(values))]
            candidates.append((err, index, max(values) * self.error_prob(err)))
        except: pass
        
    return sorted(candidates, key=lambda x: x[2], reverse=True)
        
ERRORS.__call__ = call


# In[29]:


f = open(sys.argv[1]).read()
lines = f.split('\n\n')
lines = [line.split('\n') for line in lines]
errors = [[( line.index(token), token.split(' ')[-1]) for token in line if len(token.split(' ')) > 1] 
          for line in lines]
data = [[token.split(' ')[0] for token in line] for line in lines]


# In[39]:


first = []
second = []
output_file = open(sys.argv[1].split('.')[0] + '_results.txt', 'w+')
for i in range(len(data)):
    try:
        output = errModel(data[i])
        gold = [(a[1], a[0]) for a in  errors[i]]
        try: 
            err, error_index = output[0][0:2]
            first.append(output[0][0:2] in gold)
            for j in range(error_index):
                output_file.write(data[i][j])
                output_file.write('\n')
            output_file.write(data[i][error_index] + '    ' + err)
            output_file.write('\n')
            for j in range(error_index + 1, len(data[i])):
                output_file.write(data[i][j])
                output_file.write('\n')
            output_file.write('\n')
            print(i, end='\r')
        except Exception as e:
            for j in data[i]:
                output_file.write(j)
                output_file.write('\n')
            output_file.write('\n')
        try: second.append(output[1][0:2] in gold)
        except: pass
    except: pass


# In[33]:

