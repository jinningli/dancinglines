# -*- coding: utf-8 -*-
import re
import math
from collections import Counter

WORD = re.compile(r'\w+')


def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    # print sum1, sum2, denominator, float(numerator)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def word2counter(text):
    counter = Counter()
    for i in range(len(text) / 3):

        if text[i * 3:(i + 1) * 3] in counter.keys():
            counter[text[i * 3:(i + 1) * 3]] += 1
        else:
            counter[text[i * 3:(i + 1) * 3]] = 1
    return counter


if __name__ == '__main__':
    print get_cosine(word2counter('我是'), word2counter('是谁我'))
