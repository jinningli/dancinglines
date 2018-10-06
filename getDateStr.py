import re


def getDateStr(pre_date):
    month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
             'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    # print month['Sep']
    regex = re.compile(r'(\d{2})/(\w{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2})')
    matches = re.findall(regex, pre_date)
    # print matches
    pre_date = re.sub(regex, matches[0][2] + month[matches[0][1]] + r'\1\4\5\6', pre_date)
    return pre_date


if __name__ == '__main__':
    print getDateStr('15/Jul/2016:23:47:39')
    # print getDateStr('20150713002320')
