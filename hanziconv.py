# -*- encoding=UTF-8 -*-
# ===================================================== #
# Convert Chinese(traditional) into Chinese(simplified) #
# ===================================================== #

import opencc


def conversion():
    afterSimplify = open('afterSim.txt', mode='w+')
    conversion_type = opencc.OpenCC('mix2s')
    with open('wiki.zh.txt') as preText:
        for line in preText:
            # list = []
            print type(line)
            try:
                line = line.split()
                # print line
                for word in line:
                    # print word, type(word)
                    afterWord = conversion_type.convert(word.decode('utf-8')).encode('utf-8')
                    # print afterWord, type(afterWord)
                    afterSimplify.write('{} '.format(afterWord))
                    # print
            except UnicodeDecodeError:
                pass

            afterSimplify.write('\n')
            # print '\n'
            # print after
            # break


if __name__ == '__main__':
    # cc = opencc.OpenCC('t2s')
    # line = "歐幾里得 西元前三世紀的希臘數學家 現在被認為是幾何之父 此畫為拉斐爾的作品 雅典學院 数学 "
    # print type((cc.convert(line.decode('utf-8'))).encode('utf-8'))
    # print type(line)
    conversion()
