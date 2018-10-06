# ===================================================== #
# Implementation of TF-SW                               #
# ===================================================== #

import json
import jieba
import util
import gensim
import collections
import networkx
import cosine
import word2vec
import getDateStr
import path
import math
from timeit import default_timer as timer


def cut():
    content = open(path.afterProcess_path, mode='w+')
    jieba.load_userdict('dict/event.txt')
    stopwords = [line.strip() for line in open('dict/stopwords.txt', 'rb').readlines()]
    for i in range(len(stopwords)):
        stopwords[i] = stopwords[i].decode('utf8')

    with open(path.source_path) as baidu_file:
        for line in baidu_file:
            processDict = {'cut_text': '', 'create_time': ''}
            jsonLine = json.loads(line)
            lineContent = jsonLine['text']
            segList = jieba.cut(lineContent, cut_all=False)
            segList = [word for word in segList if word not in [' '] + stopwords + util.PUCTUATION]
            processDict['create_time'] = getDateStr.getDateStr(jsonLine['create_time'])
            processDict['cut_text'] = segList
            content.write('{}\n'.format(json.dumps(processDict)))
    content.close()
    baidu_file.close()


def text_rank(dateJson, source, model, wiki_model):

    data = []

    for item in source:
        if item['create_time'][0:8] == dateJson:
            data.append(item)
    if len(data) == 0:
        return

    print '# of records:' + str(len(data))

    print data[0]['create_time']
    dict_day = collections.OrderedDict()

    Graph = networkx.Graph()

    for item in data:
        for word in item['cut_text']:
            if word not in dict_day:
                dict_day[word] = 1
            else:
                dict_day[word] += 1

    dict_day = sorted(dict_day.iteritems(), key=lambda d: d[1], reverse=True)
    print dict_day[0]

    fre_files = open(path.hotwords_path_fre.format(dateJson), 'w+')
    try:
        for i in range(len(dict_day)):
            line = {'keyword': dict_day[i][0].encode('utf-8'), 'num': str(dict_day[i][1])}
            fre_files.write('{}\n'.format(json.dumps(line, ensure_ascii=False)))
    except IndexError:
        print 'done'
    fre_files.close()

    dict_day = [item for item in dict_day if item[1] > 100]

    print 'adding edges...'

    scale = len(dict_day)
    for x in range(scale):
        for y in range(x, scale):
            if x == y:
                continue
            sim = 0.1 * cosine.get_cosine(collections.Counter(dict_day[x][0].encode('utf-8')),
                                          collections.Counter(dict_day[y][0].encode('utf-8')))
            if dict_day[x][0] in model and dict_day[y][0] in model:
                sim += 0.2 * model.similarity(dict_day[x][0], dict_day[y][0])
            if dict_day[x][0] in wiki_model and dict_day[y][0] in wiki_model:
                sim += 0.7 * wiki_model.similarity(dict_day[x][0], dict_day[y][0])
            if sim > 0:
                Graph.add_edge(x, y, weight=sim)

    print '# of nodes: ' + str(Graph.number_of_nodes())
    print '# of edges: ' + str(Graph.number_of_edges())
    print 'pageranking...'

    pr = networkx.pagerank(Graph)

    result = [[dict_day[pr.keys()[j]][0], dict_day[pr.keys()[j]][1], pr.values()[j]] for j in range(len(pr.values()))]

    sum_of_fre = sum([item[1] for item in result])

    result = sorted(result, key=lambda d: d[2], reverse=True)
    pr_file = open(path.hotwords_path_pr.format(dateJson), 'w+')
    try:
        for i in range(len(result)):
            line = {'keyword': result[i][0].encode('utf-8'), 'num': str(result[i][1]),
                    'factor': str(result[i][2])}
            pr_file.write('{}\n'.format(json.dumps(line, ensure_ascii=False)))
    except IndexError:
        print 'done'
    pr_file.close()

    result = sorted(result, key=lambda d: d[2] * d[1], reverse=True)
    hot_words_file = open(path.hotwords_path_frepr.format(dateJson), 'w+')
    try:
        for i in range(len(result)):
            line = {'keyword': result[i][0].encode('utf-8'), 'num': str(result[i][1]),
                    'factor': str(result[i][2])}
            hot_words_file.write('{}\n'.format(json.dumps(line, ensure_ascii=False)))
    except IndexError:
        print 'done'
    hot_words_file.close()


if __name__ == '__main__':
    cut()
    word2vec.word2vec()

    model = gensim.models.Word2Vec.load(path.model_path)
    wiki_model = gensim.models.Word2Vec.load('wiki.zh.text.model')

    date = []
    source_data = []

    with open(path.afterProcess_path, mode='r') as content:
        for line in content:
            data = json.loads(line)
            source_data.append(data)
            if data['create_time'][0:8] in date:
                continue
            else:
                date.append(data['create_time'][0:8])
    content.close()
    date = sorted(date)
    print date

    start = timer()
    for i in date:
        text_rank(i, source_data, model, wiki_model)
        print '{} done'.format(i)
    end = timer()
    print end - start
