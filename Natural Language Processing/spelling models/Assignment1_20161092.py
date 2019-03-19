
# coding: utf-8

# # NLP Assignment 1: Part A
# 
# * Author: Ramkishore Saravanan
# * Roll No: 20161092

# ## *NOTE: Language Models, Spell checkers have been implemented as classes instead of functions.* 
# * **Task 1: Tokeniser and Language Model**
#     * Implemented: `Laplace smoothing`, `Witten-bell` and `backoff` in `class TrigramLanguageModel`
#     * Tokeniser is passed as input to `class TrigramLanguageModel`
#     * Complete n-gram is also implemented in `class TrigramLanguageModel` as a member function `complete_ngram(...)`
# * **Task 2: Spell checker**
#     * Spell checker is implemented as a `class SpellCorrector`
#     * Spelling model is implemented in `class TrigramSpellingModel`
# * **Task 3: Grammaticality test**
#     * Uses language model created in Task 1
#    

# `no_files` is the number of files to train on. Set it to `None` to train on entire corpus.

# In[1]:


no_files = 100


# ## Task 1: Tokenisation

# In[2]:


import os
import sys
import re
import string
from operator import itemgetter
from ipy_table import *
import matplotlib.pyplot as plt


# In[3]:


from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
init_notebook_mode(connected=True)


# In[4]:


def train_model(model, no_files):
    files = os.listdir('Gutenberg/txt')[0:no_files]
    for file in files:
        print('processed: ', file, ' '*100, end='\r')
        with open('Gutenberg/txt/' + file) as f:
            model.update_lm(f.read())


# In[5]:


def make_table(d):
    print("{:<15} {:<10}".format('Input','Output'))
    print('------------------------')
    for v in d.items():
        label, num = v
        print("{:<15} {:<10}".format(label, num))


# # Tokeniser
# 
# * `tokeniser()` is a function which takes a string as input.
# * Output is a list of list of words, the former list represents a sentence.

# In[6]:


# text to test tokeniser with

# text = '''With the presence of Mr. Inglethorp, a sense of constraint and veiled
# hostility seemed to settle down upon the company. Miss Howard, in
# particular, took no pains to conceal her feelings. Mrs. Inglethorp,
# however, seemed to notice nothing unusual. Her volubility, which I
# remembered of old, had lost nothing in the intervening years, and she
# poured out a steady flood of conversation, mainly on the subject of the
# forthcoming bazaar which she was organizing and which was to take place
# shortly. Occasionally she referred to her husband over a question of
# days or dates. His watchful and attentive manner never varied. From the˘
# very first I took a firm and rooted dislike to him, and I flatter myself
# that my first judgments are usually fairly shrewd.
#
# Presently Mrs. Inglethorp turned to give some instructions about letters
# to Evelyn Howard, and her husband addressed me in his painstaking voice:
#
# "Is soldiering your regular profession, Mr. Hastings?"
#
# "No, before the war I was in Lloyd's."
#
# "And you will return there after it is over?"
#
# "Perhaps. Either that or a fresh start altogether."
#
# Mary Cavendish leant forward.'''


# In[7]:


def sentence_tokeniser(text):
    split = '<split>'
    patterns = [
        # multiple new line characters
        (re.compile('(\.? *\n\n+)'), split),
        # dots after Honorifics etc which dont mean EOL
        (re.compile('(?<![(Mr)(MR)(mr)(Mrs)(MRS)(Dr)(Ms)(i\.e)(etc)(\d)(A-Z)])\.'), split),
        # other dots which don;t follow honorifics.
        (re.compile('(?<=[a-z ][a-z][a-z])\.'), split),
         ]
    for regex, subs in patterns:
        sentences = regex.sub(subs, text)   #inse
    sentences = sentences.split('<split>')
    sentences = list(filter(lambda a: len(a)>0, sentences))


    return sentences


# ## Testing Sentence Tokeniser

# In[8]:


# sentence_tokeniser(text)


# In[9]:


def word_tokeniser(text):
    split = '<split>'
    # '.' was taken care of in sentence tokeniser
    patterns = [
        (re.compile('[^A-Za-z\.]'), split)
    ]
    for regex, subs in patterns:
        words = regex.sub(subs, text)   #inse
    words = words.split('<split>')
    words = list(filter(lambda a: len(a)>0, words))
    return words


# In[10]:


def tokeniser(text):
    sentences = sentence_tokeniser(text)
    words = []
    for sentence in sentences:
        words.append(word_tokeniser(sentence))
    return words


# ## Testing word tokeniser

# In[11]:


# print(tokeniser(text))


# ## Language Model and Smoothing

# In[12]:


class TrigramLanguageModel():
    
    def __init__(self, tokeniser=None):
        self.tree = {}
  #      self.vocab = {}
  #      self.inv_vocab = {}
        self.no_words = 0
        self.total_trigrams = 0.0
        
        if tokeniser is not None: self.tokeniser = tokeniser
        else: self.tokeniser = self.__naive_tokeniser
    
    def __naive_tokeniser(self, text):
        '''Input:  String
           Output: List of tokens'''
        # naive line splitter: multiple new line chars, may be preceeded by a dot and/or space
        lines = re.split(r'(\.? *\n\n+)', text)

        # naive word splitter: multiple spaces, tabs, `: , & : ( ) - ' "`
        lines = [list(filter(is_not_delimiter, re.split(r'( +)|(\n)|(\t)|(;|,|&|:|\(|\)|-|\'|\")+', line))) 
                for line in lines]

        # remove lists with characters less than 1
        lines = list(filter(lambda a: len(a)>1, lines))
  #      lines = [l + ['<end>'] for l in lines]
  #      lines = [['<start>'] + l for l in lines]
        return lines
    
    def __update_tree(self, trigram):
        
        w1, w2, w3 = trigram
        if w1 in self.tree:
            if w2 in self.tree[w1]: 
                if w3 in self.tree[w1][w2]: self.tree[w1][w2][w3] += 1
                else: self.tree[w1][w2][w3] = 1
            else: self.tree[w1][w2] = {w3:1}
        else: self.tree[w1] = {w2:{w3:1}}
        self.total_trigrams += 1
    
    def update_lm(self, text):
        '''Input: Untokenised text(string)
           Updates language model with this text.'''
        tokenised_text = self.tokeniser(text)
        trigrams = self.get_trigrams(tokenised_text)
        [self.__update_tree(t) for t in trigrams]
        
    def get_trigrams(self, tokenised_text, indices=True):
        '''Input: tokenised_text
                  indices: Returns indices of words if True
           Output: List of trigrams
        '''
        trigrams = []
        for line in tokenised_text:
            for i in range(len(line) - 2):
                trigrams.append([line[i],
                                 line[i+1],
                                 line[i+2]])
        return trigrams
    
    # def __update_vocab(self, tokenised_text):
    #     for line in tokenised_text:
    #         for word in line:
    #             if word not in self.vocab:
    #                 self.vocab[word], self.no_words = self.no_words, self.no_words + 1
    #                 self.inv_vocab[self.no_words - 1] = word
    #
    # def complete_ngram(self, bigram, no=10):
    #     '''Predicts next word based on the last two words in the sentence
    #     '''
    #     w1, w2 = bigram[-2:]
    #     d = sorted(self.tree[w1][w2].items(), key=itemgetter(1), reverse=True)[0:no]
    #     words = [self.inv_vocab[w[0]] for w in d]
    #     counts = [i[1] for i in d]
    #     iplot([{"x": words, "y": counts}])
    #     return words
    
    def get_probability(self, sentence):
        '''Returns probability of sentence(string)
        '''
        tokenised = self.tokeniser(sentence)
        trigrams = self.get_trigrams(tokenised, indices=True)
        counts = []
        denominators = []
        for t in trigrams:
            try:
                # counts = p(w1, w2, w3) * total_trigrams
                counts.append(self.tree[t[0]][t[1]][t[2]])
                # denominator = p(w1, w2) * total trigrams
                denominators.append(sum(i[1] for i in self.tree[t[0]][t[1]].items()))
            except Exception as e:
                counts.append(0.1)
                denominators.append(1)
        prob = 1.0
        for i, j in zip(counts, denominators):
            prob *= i/j
        return prob
    
    def laplace_smoothing(self, sentence):
  
        tokenised = self.tokeniser(sentence)
        trigrams = self.get_trigrams(tokenised, indices=True)
        counts = []
        denominators = []
        for t in trigrams:
            # Add 1 to numerator
            try: counts.append(self.tree[t[0]][t[1]][t[2]] + 1)
            except Exception as e: counts.append(1)
            # Add len(vocab) + 1 to denominator
            try: denominators.append(sum([i[1] for i in self.tree[t[1]][t[2]].items()]) + len(self.total_trigrams) + 1)
            except: denominators.append(self.total_trigrams + len(self.vocab) + 1)
        prob = 1.0
        for i, j in zip(counts, denominators):
            prob *= i/j
        return prob
        
    def witten_bell_smoothing(self, sentence):
        
        tokenised = self.tokeniser(sentence)
        trigrams = self.get_trigrams(tokenised, indices=True)

        tri_counts = []
        bi_counts = []
        tri_denominators = []
        bi_denominators = []
        unique_wi = []
        sigma_wi = []
        lambda_ = []
        
        for t in trigrams:
            # Numerator for trigram prob
            try: tri_counts.append(self.tree[t[0]][t[1]][t[2]])
            except: tri_counts.append(1)
            # Numerator for bigram prob
            try: bi_counts.append(sum([i[1] for i in self.tree[t[1]][t[2]].items()]))
            except: bi_counts.append(1)
            # No. of unique elements following bigram w(i-1) and w(i-2)
            try: unique_wi.append(len(self.tree[t[0]][t[1]]))
            except: unique_wi.append(1)
            # Used in calculation of lambda
            try: sigma_wi.append(sum([i[1] for i in self.tree[t[1]][t[2]].items()]))
            except: sigma_wi.append(1)
            # Denominator for trigram prob
            try: tri_denominators.append(sum([i[1] for i in self.tree[t[1]][t[2]].items()]))
            except: tri_denominators.append(self.total_trigrams)
            # Denominator for trigram prob
            try: bi_denominators.append(sum([sum([i[1] for i in self.tree[t[1]][w].items()]) for w in self.tree[t1]]))
            except: bi_denominators.append(self.total_trigrams)
            # Lambda calculation
            lambda_ = [1.0 - i/(i+j) for i,j in zip(unique_wi, sigma_wi)]
        prob = 1.0
        for bi_n, bi_d, tri_n, tri_d, lam in zip(bi_counts, bi_denominators, tri_counts, tri_denominators, lambda_):
            prob *= (lam * tri_n/tri_d + (1-lam) * bi_n/bi_d)
        return prob
    
    def backoff(self, sentence):
        
        tokenised = self.tokeniser(sentence)
        trigrams = self.get_trigrams(tokenised, indices=True)
        
        counts = []
        denominators = []
        alpha = []
        for t in trigrams:
            # try trigram
            try: 
                counts.append(self.tree[t[0]][t[1]][t[2]])
                denominators.append(sum([i[1] for i in self.tree[t[1]][t[2]].items()]))
                alpha.append(1)
            except:
                # if not found, try bigram
                try:
                    counts.append(sum([i[1] for i in self.tree[t[1]][t[2]].items()]))
                    denominators.append(sum([sum([i[1] for i in self.tree[t[1]][w].items()]) for w in self.tree[t1]]))
                    alpha.append(0.4)
                except:
                    # else try unigram
                    try:
                        counts.append(sum([sum([i[1] for i in self.tree[t[1]][w].items()]) for w in self.tree[t1]]))
                    except:
                        counts.append(1)
                    denominators.append(len(self.tree))
                    alpha.append(0.16)
        
        prob = 1.0
        for i, j, k in zip(counts, denominators, alpha):
            prob *= k * i / j
        return prob


# In[13]:


# l = TrigramLanguageModel(tokeniser=tokeniser)


# In[14]:


# train_model(l)


# In[15]:


# def get_freq_ngrams(most=True):
#     if most: w1, w2, w3, p = [[0 for _ in range(10)] for _ in range(4)]
#     else: w1, w2, w3, p = [[100000000000 for _ in range(10)] for _ in range(4)]
#     for i in l.tree:
#         for j in l.tree[i]:
#             for k in l.tree[i][j]:
#                 for m in range(10):
#                     a = l.tree[i][j][k] > p[m]
#                     if not most: a = not a
#                     if a:
#                         w1[m], w2[m], w3[m], p[m] = i, j, k, l.tree[i][j][k]
#                         break
#     for i in range(10):
#         w1[i], w2[i], w3[i] = l.inv_vocab[w1[i]], l.inv_vocab[w2[i]], l.inv_vocab[w3[i]]
#         print(w1[i], w2[i], w3[i])


# ### Most frequent trigrams

# In[16]:


# get_freq_ngrams(True)


# ### Least frequent trigrams

# In[17]:


# get_freq_ngrams(False)


# ### N-gram frequency plot
# * I was having memory problems with `iplot` function, so used matplotlib to plot graphs.

# In[18]:


# counts = []
# words = []
# for i in l.tree:
#     for j in l.tree[i]:
#         for k in l.tree[i][j]:
#             counts.append(l.tree[i][j][k])
#             words.append(l.inv_vocab[i]+' '+l.inv_vocab[j]+' '+l.inv_vocab[k])
# x, y = zip(*sorted(zip(words, counts), key=lambda x: x[1], reverse=True)[0:100000])
# iplot([{"x": x, "y":y}])   # Only for first 1,00,000 most frequent trigrams
# plt.plot(sorted(counts, reverse=True))  # All trigrams
#
#
# # ### N-gram frequency log-log plot (Zipf's curve)
#
# # In[19]:
#
#
# plt.loglog(range(len(counts)), sorted(counts, reverse=True))
#
#
# # ### Complete n-gram
# # * Parameters:
# #     * Array containing previous words in that order
# #     * `no`: no of words to output. `default=10`
#
# # In[20]:
#
#
# l.complete_ngram(['I','have', 'an'], no=10)


# ### Grammaticality of sentence

# In[21]:


# l.laplace_smoothing('I have a child'), l.laplace_smoothing('child I have a')


# In[22]:


# l.get_probability('I have a child'), l.get_probability('child I have a')


# In[23]:


# l.witten_bell_smoothing('I have a child'), l.witten_bell_smoothing('child I have a')


# In[24]:


# l.backoff('I have a child'), l.backoff('child I have a')


# ## Task 2:  Unigrams & Spelling Detection/Correction

# * Spell checker is implemented as a `class SpellCorrector`
# * Spelling model is implemented in `class TrigramSpellingModel`

# In[25]:


class TrigramSpellingModel():
    def __init__(self, tokeniser=None):
        self.tree = {}
        self.no_words = 0
        self.total_trigrams = 0
        
        if tokeniser is not None: self.tokeniser = tokeniser
        else: self.tokeniser = self.__naive_tokeniser
    
    def __naive_tokeniser(self, text):
        '''Input:  String
           Output: List of tokens'''
        # naive line splitter: multiple new line chars, may be preceeded by a dot and/or space
        lines = re.split(r'(\.? *\n\n+)', text)

        # naive word splitter: multiple spaces, tabs, `: , & : ( ) - ' "`
        lines = [list(filter(is_not_delimiter, re.split(r'( +)|(\n)|(\t)|(;|,|&|:|\(|\)|-|\'|\")+', line))) 
                for line in lines]

        # remove lists with characters less than 1
        lines = list(filter(lambda a: len(a)>1, lines))
        return lines
    
    def __update_tree(self, trigram):
        
        w1, w2, w3 = trigram
        if w1 in self.tree:
            if w2 in self.tree[w1]: 
                if w3 in self.tree[w1][w2]: self.tree[w1][w2][w3] += 1
                else: self.tree[w1][w2][w3] = 1
            else: self.tree[w1][w2] = {w3:1}
        else: self.tree[w1] = {w2:{w3:1}}
        self.total_trigrams += 1
    
    def update_lm(self, text):
        
        tokenised_text = self.tokeniser(text)
        trigrams = self.get_trigrams(tokenised_text)
        [self.__update_tree(t) for t in trigrams]
        
    def get_trigrams(self, tokenised_text):
        
        trigrams = []
        for line in tokenised_text:
            for word in line:
                for i in range(len(word) - 2):
                    trigrams.append([word[i],
                                    word[i+1],
                                    word[i+2]])
        return trigrams
    
    def get_probability(self, word):
        
        if len(word) < 3:
            return float(sum([self.tree[word[0]][word[1]][i] for i in self.tree[word[0]][word[1]]]))/self.total_trigrams
        trigrams = self.get_trigrams([[word]])
        counts = []
        denominators = []
        for t in trigrams:
            try:
                counts.append(self.tree[t[0]][t[1]][t[2]])
                denominators.append(sum(i[1] for i in self.tree[t[0]][t[1]].items()))
            except Exception as e:
                counts.append(0)
                denominators.append(1)
        prob = 1.0
        for i, j in zip(counts, denominators):
            prob *= i/j
        return prob


# In[26]:


# b = TrigramSpellingModel(tokeniser=tokeniser)


# In[27]:


# train_model(b)


# **Some sample probabilities**
# 

# In[28]:


# b.get_probability("late")


# In[29]:


# words = ['lati', 'late', 'an', 'man', 'girla', 'girly', 'chila', 'chile', 'child']
# d = {}
# for i in words:
#     d[i] = b.get_probability(i)
# make_table(d)


# In[30]:


class SpellCorrector():
    '''self.correct(): replaces lowest scoring trigram
       self.correct2(): checks every possible replacement'''
    def __init__(self):
        self.vocab = string.ascii_letters

    def checker(self, word, lm):
        trigrams = lm.get_trigrams([[word]])
        prob = [lm.get_probability(t) for t in trigrams]
        mistake_index = prob.index(min(prob)) + 2
        return mistake_index

    def corrector(self, word, index, lm):
        ini_p = lm.get_probability(word)
        if ini_p > 10e-2:
            return word
        ch = word[index]
        for char in self.vocab:
            word = self.replace_str_index(word, index, char)
            prob = lm.get_probability(word)
            if prob > ini_p:
                ini_p, ch = prob, char
        
        word = self.replace_str_index(word, index, ch)
        return word
            
    def correct(self, word, lm):
        index = self.checker(word, lm)
        return self.corrector(word, index, lm)
    
    def correct2(self, word, lm):
        possibilities = [self.corrector(word, index, lm) for index in range(len(word))]
        probs = [lm.get_probability(w) for w in possibilities]
        return possibilities[probs.index(max(probs))]
            
    
    def replace_str_index(self, text,index=0,replacement=''):
        return '%s%s%s'%(text[:index],replacement,text[index+1:])


# In[31]:


# a = SpellCorrector()


# ## Some examples from Spell checker

# In[32]:


# incorrect_words = ['latk', 'veay', 'plua', 'waq', 'ice', 'hkr']
# d = {}
# for w in incorrect_words:
#     d[w] = a.correct2(w, b)
# make_table(d)


# ## Grammaticallity test

# In[33]:


def score_grammaticality(sentence, model):
    return {'normal': model.get_probability(sentence),
            'laplace': model.laplace_smoothing(sentence),
            'witten_bell_smoothing': model.witten_bell_smoothing(sentence),
            'backoff': model.backoff(sentence)}


# In[34]:

#
# score_grammaticality('I have a child', l)
#
#
# # In[35]:
#
#
# score_grammaticality('child I have a', l)

