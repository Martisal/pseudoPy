import Stemmer
import re
import statistics
from nltk.translate.bleu_score import sentence_bleu
from similarityMetrics.use_score_v import use

with open('summaries/test.out.tokenized', 'r') as f:
    out = f.readlines()

with open('summaries/test.out.tokenized.1st', 'r') as f:
    out1 = f.readlines()

with open('summaries/test.target.tokenized', 'r') as f:
    tg = f.readlines()    

#lowercase
out = [s.lower() for s in out]
out1 = [s.lower() for s in out1]
tg = [s.lower() for s in tg]

#remove punctuation
out = [re.sub(r'[^\w\s]', '', s).replace('  ', ' ') for s in out]
out1 = [re.sub(r'[^\w\s]', '', s).replace('  ', ' ') for s in out1]
re = [re.sub(r'[^\w\s]', '', s).replace('  ', ' ') for s in tg]

#stemming
stemmer = Stemmer.Stemmer('english')

out = [stemmer.stemWords(s.split()) for s in out]
out1 = [stemmer.stemWords(s.split()) for s in out1]
tg = [stemmer.stemWords(s.split()) for s in tg]

use(tg, out1, 11111)


"""
scores1 = []
scores2 = []
for i, t in enumerate(tg):
    scores1.append(sentence_bleu([t.split()], out[i].split(), weights=(1,0,0,0)))
    scores2.append(sentence_bleu([t.split()], out[i].split(), weights=(0.5, 0.5,0,0)))

print('BLEU score for out:', statistics.mean(scores1), statistics.mean(scores2))

scores1 = []
scores2 = []
for i, t in enumerate(tg):
    scores1.append(sentence_bleu([t.split()], out1[i].split(), weights=(1,0,0,0)))
    scores2.append(sentence_bleu([t.split()], out1[i].split(), weights=(0.5, 0.5,0,0)))

print('BLEU score for out1st', statistics.mean(scores1), statistics.mean(scores2))
"""

