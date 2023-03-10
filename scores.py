import sys
import pickle
import numpy as np
import os
import argparse
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

#custom
import Stemmer
import re
import statistics
from nltk.translate.bleu_score import sentence_bleu
import simmetrics


def fil(com):
    ret = list()
    for w in com:
        if not '<' in w:
            ret.append(w)
    return ret

def use(reflist, predlist, batchsize):
    import tensorflow_hub as tfhub

    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    model = tfhub.load(module_url)
    refs = list()
    preds = list()
    count = 0
    for ref, pred in zip(reflist, predlist):
        ref = ' '.join(ref).strip()
        pred = ' '.join(pred).strip()
        if pred == '':
            count+=1
            continue
        refs.append(ref)
        preds.append(pred)

    total_csd = np.zeros(count)
    for i in range(0, len(refs),batchsize):
        ref_emb = model(refs[i:i+batchsize])
        pred_emb = model(preds[i:i+batchsize])
        csm = cosine_similarity_score(ref_emb, pred_emb)
        csd = csm.diagonal()
        total_csd = np.concatenate([total_csd, csd])
    avg_css = np.average(total_csd)

    ret = ('for %s functions\n' % (len(predlist)))
    ret+= 'Cosine similarity score with universal sentence encoder embedding is %s\n' % (round(avg_css*100, 2))
    return ret

def cosine_similarity_score(x, y):
    from sklearn.metrics.pairwise import cosine_similarity
    cosine_similarity_matrix = cosine_similarity(x, y)
    return cosine_similarity_matrix

def prep_dataset(reffile, predfile, batchsize):
    preds = dict()
    predicts = open(predfile, 'r')
    for c, line in enumerate(predicts):
        (fid, pred) = line.split('\t')
        fid = int(fid)
        pred = pred.split()
        pred = fil(pred)
        preds[fid] = pred
    predicts.close()

    refs = list()
    newpreds = list()
    d = 0
    targets = open(reffile, 'r')
    for line in targets:
        (fid, com) = line.split(',')
        fid = int(fid)
        com = com.split()
        com = fil(com)

        if len(com) < 1:
            continue
        try:
            newpreds.append(preds[fid])
        except Exception as ex:
            continue

        refs.append(com)

    print('final status')
    score = use(refs, newpreds, batchsize)
    return score

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    #parser.add_argument('input', type=str, default=None)
    parser.add_argument('--coms-filename', dest='comsfilename', type=str, default='coms.test')
    parser.add_argument('--batchsize', dest='batchsize', type=int, default=50000)
    parser.add_argument('--gpu', dest='gpu', type=str, default='')
    parser.add_argument('--challenge', action='store_true', default=False)
    parser.add_argument('--vmem-limit', dest='vmemlimit', type=int, default=0)
    args = parser.parse_args()
    #predfile = args.input
    comsfile = args.comsfilename
    batchsize = args.batchsize
    gpu = args.gpu
    challenge = args.challenge
    vmemlimit = args.vmemlimit

    os.environ['CUDA_VISIBLE_DEVICES'] = gpu
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)

    if(vmemlimit > 0):
        if gpus:
            try:
                tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=vmemlimit)])
            except RuntimeError as e:
                print(e)
    
    #score = prep_dataset(comsfile, predfile, batchsize)
    
    with open('../summaries/test.out.tokenized', 'r') as f:
        out = f.readlines()
    
    with open('../summaries/test.out.tokenized.1st', 'r') as f:
        out1 = f.readlines()
    
    with open('../summaries/test.target.tokenized', 'r') as f:
        tg = f.readlines()
    
    #lowercase
    out = [s.lower() for s in out]
    out1 = [s.lower() for s in out1]
    tg = [s.lower() for s in tg]
    
    #remove punctuation
    out = [re.sub(r'[^\w\s]', '', s).replace('  ', ' ') for s in out]
    out1 = [re.sub(r'[^\w\s]', '', s).replace('  ', ' ') for s in out1]
    re = [re.sub(r'[^\w\s]', '', s).replace('  ', ' ') for s in tg]
    
    print('Sentence embedding, out1st')
    score = use(out1, tg, 11111)
    print(score)
    print()
    print('Sentence embedding, out')
    score = use(out, tg, 11111)
    print(score)

    #stemming
    stemmer = Stemmer.Stemmer('english')
    
    out = [stemmer.stemWords(s.split()) for s in out]
    out1 = [stemmer.stemWords(s.split()) for s in out1]
    tg = [stemmer.stemWords(s.split()) for s in tg]    

    print()
    print('BLEU, out1st')
    score = simmetrics.all_bleu_score(tg, out1)
    print(score)
    print()
    print('BLEU, out')
    score = simmetrics.all_bleu_score(tg, out)
    print(score)

    print()
    print('ROUGE, out1st')
    score = simmetrics.all_rouge_score(tg, out1)
    print(score)
    print()
    print('ROUGE, out')
    score = simmetrics.all_rouge_score(tg, out)
    print(score)

