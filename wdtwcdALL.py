# -*- coding: utf-8 -*-
"""
@author: Weiming Bao
"""

# ===================================================== #
# Implementation of wDTW-CD                             #
# EPTS of all datasets except Pokemon GO are enveiled.  #
# We still try to remove confidencial info for demo.    #
# ===================================================== #


import wdtwcd

from numpy import array, round, arange
from numpy.linalg import norm
from matplotlib import pylab as plt
from matplotlib.pylab import savefig


if __name__ == '__main__':
    dtw_result = open('dtw_result.csv', 'a+')

    # ---------------------------------------------
    # dfzx
    # areax_xtick_labels = ['0.00','0.05', '0.10','0.15','0.20','0.25','0.30','0.35']
    # alphago
    areax_xtick_labels = ['0.00', '0.05', '0.10', '0.15', '0.20', '0.25', '0.30', '0.35', '0.40', '0.45', '0.50', '0.55',
                          '0.60', '0.65', '0.70']
    # ====================  end ===================

    ch = 1

    while (ch<=10):
        # choice = ch % 10
        # if choice == 0:
        #     choice = 10
        choice = ch
        evName = (ch-1) / 10

        # ==============================================
        namelist = [
        # 'dfzx', 'stock', 'AlphaGo', 'leo', 'kobe', 'linxinru', 'brexit', 
        'PokemonGO'
        # , 'nanhai'
        ]
        name = namelist[evName]

        # ==================== date ====================
        # dfzx
        datelist = [
                    # stock market crash
                    # AlphaGO
                    # leo
                    # kobe
                    # Linxinru
                    # Brexit
                    # Pokemon GO
            ['20160701','20160702','20160703','20160704','20160705','20160706','20160707','20160708','20160709','20160710','20160711','20160712','20160713','20160714','20160715','20160716','20160717','20160718','20160719','20160720']
                    # nanhai
                    ]

        date = datelist[evName]
        # ====================  end ====================

        # ==================== weibo ====================
        # dfzx
        weibolist = [
        # stock market crash
        # AlphaGO
        # leo
        # kobe
        # Linxinru
        # Brexit
        # Pokemon GO
            [2.55415044372e-05,4.29692419183e-05,0,0,6.24946827943e-05,0.00664536752519,0.116231125816,0.228259570801,0.0294646634886,0.015552690231,0.0805871151817,0.308299364699,0.0596006095288,0.0362482371806,0.0237630519132,0.00697945460431,0.0372065914012,0.0322850230814,0.0121110531251,0.006635075993]
        # nanhai
        ]
        # ====================  end ====================

        # ==================== baidu ====================
        # dfzx
        baidulist = [
        # stock market crash
        # AlphaGO
        # leo
        # kobe
        # Linxinru
        # Brexit
        # Pokemon GO
            [0.000586257611449,0.000541714866194,0.000429505820208,0.000583044380151,0.00055530291712,0.0299118864067,0.0466684934186,0.083147184066,0.0573964479784,0.055413364941,0.130156395305,0.105181185079,0.0852123705643,0.0762249965497,0.0714844832561,0.0491101311512,0.0434961040883,0.0484384837787,0.0453813147392,0.0700813330828]
        # nanhai
        ]
        # ====================  end ====================

        xsel = weibolist[evName]
        x = array(xsel).reshape(-1, 1)
        ysel = baidulist[evName]
        y = array(ysel).reshape(-1, 1)
        print x.mean()
        print y.mean()


        # data-formating
        datefor = list();
        for item in date:
            item = item[4] + item[5] + '/' + item[6] + item[7]
            datefor.append(item)


        if choice == 1:
            method = '0DTW'
        elif choice == 2:
            method = '1DTWbias'
        elif choice == 3:
            method = '2DDTW'
        elif choice == 4:
            method = '3DDTWbias'
        elif choice == 5:
            method = '4wDTW'
        elif choice == 6:
            method = '5wDDTW'
        elif choice == 7:
            method = '6wDTW-CD1'
        elif choice == 8:
            method = '7wDTW-CD2'
        elif choice == 9:
            method = '8wDTW-CD3'
        else:
            method = '9DTW-CD'

        # dtw
        dist, cost, acc, path, xd, yd = wdtwcd(choice, x, y, dist=lambda x, y: norm(x - y, ord=1))
        print 'Minimum distance found:', dist
        print path

        # visualization --matplotlib
        x1 = round(x, 5)
        y1 = round(y, 5)
        xlist = list()
        for i in range(x1.shape[0]):
            xlist.extend(x1[i])
        ylist = list()
        for i in range(y1.shape[0]):
            ylist.extend(y1[i])

        left_x, left_y = 0.1, 0.12
        width, height = 0.65, 0.65
        left_xh = left_x + width + 0.02
        left_yh = left_y + height + 0.02

        hotarea = [left_x, left_y, width, height]
        hist_x = [left_xh, left_y, 0.19, height]
        hist_y = [left_x, left_yh, width, 0.19]
        colbar = [left_x, 0.035, width, 0.015]

        plt.style.use('seaborn-bright')
        plt.rc('font', **{'family': 'serif', 'serif': 'Times New Roman'})
        plt.rc('text', usetex=True)
        plt.figure(1, figsize=(8, 8))

        areahot = plt.axes(hotarea)
        areax = plt.axes(hist_x)
        areay = plt.axes(hist_y)
        cbarax = plt.axes(colbar)

        im = areahot.imshow(acc.T, origin='lower', cmap=plt.cm.hot, interpolation='nearest')
        plt.colorbar(im, cax=cbarax, orientation='horizontal')

        areahot.plot(path[0], path[1], '-ow')
        areahot.set_xlim(-0.5, acc.shape[0] - 0.5)
        areahot.set_ylim(-0.5, acc.shape[1] - 0.5)
        areahot.set_xticks(arange(acc.shape[0]))
        areahot.set_xticklabels(datefor, rotation=60)
        areahot.set_yticks(arange(acc.shape[1]))
        areahot.set_yticklabels(datefor)

        areax.plot(y, arange(acc.shape[1]), '-ob',label = "Baidu")
        areay.plot(x, '-or', label = "Weibo")
        areax.set_ylim(areahot.get_ylim())
        areax.set_xlim(areay.get_ylim())
        areax.set_xticklabels(areax_xtick_labels, rotation=90)
        areay.set_xlim(areahot.get_xlim())
        areax.set_yticks([])
        areay.set_xticks([])
        areax.legend()
        areay.legend()
        # plt.show()
        savefig(name + '-' + method + '-' + 'heatmap.pdf')
        plt.close()

        # metrics
        patha = path[0]
        pathb = path[1]
        pathadelta = list()
        pathbdelta = list()
        for i in range(len(patha) - 1):
            pathadelta.append(patha[i + 1] - patha[i])
        for i in range(len(pathb) - 1):
            pathbdelta.append(pathb[i + 1] - pathb[i])
        cnter = 0
        wflag = 0
        wneg = 0
        wpos = 0
        for i in range(len(patha) - 1):
            if (pathadelta[i] == 0):
                if (wflag == 0):
                    wflag = 1
                if (cnter < 0):
                    wneg += abs(cnter)
                    cnter += 1
                else:
                    cnter += 1
                    wpos += abs(cnter)
            elif (pathbdelta[i] == 0):
                if (wflag == 0):
                    wflag = -1
                if (cnter > 0):
                    wpos += abs(cnter)
                    cnter -= 1
                else:
                    cnter -= 1
                    wneg += abs(cnter)
            else:
                flag = 0
                if (cnter > 0):
                    wpos += cnter
                elif (cnter < 0):
                    wneg -= cnter
        # print wpos
        # print wneg

        dissum = 0.0
        disdtw = 0.0
        for i in range(len(patha)):
            dissum += 0.5 * abs(x[patha[i]] - y[pathb[i]]) * abs(xd[patha[i]] - yd[pathb[i]])
            dissum += 0.5 * ((patha[i] - pathb[i]) / (len(x) + len(y))) ** 2.0
            disdtw += (abs(x[patha[i]] - y[pathb[i]]) * abs(xd[patha[i]] - yd[pathb[i]]))**0.5
        dissum = ((dissum / len(patha))** 0.5)/ len(patha) * len(x)
        disdtw = disdtw / (len(patha)) * len(x)

        # print 'DTW distance: ', disdtw[0]
        # print 'Time-irrelevant similarity: ', 1.0 - disdtw[0]
        # # print 'Pos Time-warping degree: ', (float(wpos) / ((max(patha) + 1) * (max(patha)-1)))
        # # print 'Neg Time-warping degree: ', (float(wneg) / ((max(patha) + 1) * (max(patha)-1)))
        # # print 'Time-warping degree: ', (float(wpos + wneg) / ((max(patha) + 1) * (max(patha)-1)))
        # print 'Pos Time-warping degree: ', (float(wpos) / ((len(x)-1)*(len(x)-2)))
        # print 'Neg Time-warping degree: ', (float(wneg) / ((len(x)-1)*(len(x)-2)))
        # print 'Time-warping degree: ', (float(wpos + wneg) / ((len(x)-1)*(len(x)-2)))
        # print 'Overall similarity: ', dissum[0]

        dtw_result.write(name + ',' + method + ',' + str(len(date)) + ',' + str(len(patha)) + ','
                         + str(disdtw[0]) + ',' + str(1.0 - disdtw[0]) + ','
                         + str(wpos) + ',' + str(wneg) + ',' + str(float(wpos + wneg) / ((len(x)-1)*(len(x)-2))) + ','
                         + str(dissum[0]) + ',' + str(1.0 - dissum[0]) + '\n')

        plt.plot(x, 'r', label = "Weibo")
        plt.plot(y, 'b', label = "Baidu")
        plt.legend()
        for i in range(len(patha)):
            plt.plot([patha[i], pathb[i]], [x[patha[i]], y[pathb[i]]], 'k-o')
        # plt.show()
        savefig(name + '-' + method + '-' + 'match.pdf')
        plt.close()

        pa = list()
        pb = list()
        for i in range(len(patha)):
            pa.append(x[patha[i]])
        for i in range(len(pathb)):
            pb.append(y[pathb[i]])

        plt.plot(range(len(pa)), pa, 'r-o', label = "Weibo")
        plt.plot(range(len(pb)), pb, 'b-o', label = "Baidu")
        plt.legend()
        # plt.show()
        savefig(name + '-' + method + '-' + 'aligned.pdf')
        plt.close()

        print (name + '-' + method)

        ch += 1
