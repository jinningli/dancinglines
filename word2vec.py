# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:26:39 2016

@author: Eric
"""

import gensim
import json
import path
from timeit import default_timer as timer


def word2vec():
    sentences = []
    with open(path.afterProcess_path, 'r') as fin:
        for line in fin:
            obj = json.loads(line)
            if obj[u'cut_text']:
                sentences.append(obj[u'cut_text'])

    print 'start to train...'
    start = timer()
    model = gensim.models.Word2Vec(sentences, size=100, min_count=5)
    end = timer()
    print end - start
    model.save(path.model_path)
    # model = gensim.models.Word2Vec.load('dongfangzhixing_weibo_model')
    #
    # print model.most_similar(u'东方之星', topn=5)[0][0], model.most_similar(u'东方之星', topn=5)[0][1]
    # print model.most_similar(u'东方之星', topn=5)[1][0]
    # print model.most_similar(u'东方之星', topn=5)[2][0]
    # print model.most_similar(u'东方之星', topn=5)[3][0]
    # print model.most_similar(u'东方之星', topn=5)[4][0]
    # model.save('dongfangzhixing_weibo_model')


if __name__ == '__main__':
    print 1
    word2vec()
