class TrigramLanguageModel():
    
    def __init__(self, tokeniser=None):
        self.tree = {}
        self.vocab = {}
        self.inv_vocab = {}
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
    
    def update_tree(self, trigram):
        
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
        self.__update_vocab(tokenised_text)
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
                if indices:
                    try: w1 = self.vocab[line[i]]
                    except: w1 = '<unk>'
                    try: w2 = self.vocab[line[i+1]]
                    except: w2 = '<unk>'
                    try: w3 = self.vocab[line[i+2]]
                    except: w3 = '<unk>'
                    trigrams.append([w1, w2, w3])
                else:
                    trigrams.append([line[i],
                                     line[i+1],
                                     line[i+2]])
        return trigrams
    
    def __update_vocab(self, tokenised_text):
        for line in tokenised_text:
            for word in line:
                if word not in self.vocab:
                    self.vocab[word], self.no_words = self.no_words, self.no_words + 1
                    self.inv_vocab[self.no_words - 1] = word
                    
    def complete_ngram(self, bigram, no=10):
        '''Predicts next word based on the last two words in the sentence
        '''
        w1, w2 = bigram[-2:]
        w1, w2 = self.vocab[w1], self.vocab[w2]
        d = sorted(self.tree[w1][w2].items(), key=itemgetter(1), reverse=True)[0:no]
        words = [self.inv_vocab[w[0]] for w in d]
        counts = [i[1] for i in d]
        iplot([{"x": words, "y": counts}])
        return words
    
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
                counts.append(0)
                denominators.append(1)
        prob = 1.0
        for i, j in zip(counts, denominators):
            prob *= i/j
        return prob
    
    def get_prob(self, t):
        try: return self.tree[t[0]][t[1]][t[2]] / sum(self.tree[t[0]][t[1]].values())
        except Exception as e:
            return 1./self.total_trigrams
    
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

def null_tokenizer(s):
    return s