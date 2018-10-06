# ===================================================== #
# Calculate, normalize and format EPTS of the time span #
# ===================================================== #


import path
import json
import os
import re
import math


def pop_accu():
    with open(path.event_dir + 'popularity_' + path.data_name + '.json', mode='w+') as output:
        for file_name in os.listdir(path.path_data_dir):
            popu = 0.0
            fre = 0
            line_cnt = 0
            with open(path.path_data_dir + file_name) as content:
                for line in content:
                    json_line = json.loads(line)
                    popu += float(json_line['num']) * float(json_line['factor'])
                    fre += int(json_line['num'])
                    line_cnt += 1
            content.close()
            line2write = {'date': re.findall('[0-9]+', str(file_name))[0][4:],
                          'fre': str(fre),
                          'scale': str(line_cnt),
                          'popuraw': str(popu),
                          'popumax': str(popu * fre),
                          'popu2': str(popu * fre / (line_cnt ** 0.2)),
                          'popu5': str(popu * fre / (line_cnt ** 0.5)),
                          'popu8': str(popu * fre / (line_cnt ** 0.8)),
                          'popu': str(popu * fre / line_cnt),
                          'popu_scale': str(popu * line_cnt)}
            output.write('{}\n'.format(json.dumps(line2write, ensure_ascii=False)))
    output.close()


def pop_norm():
    popuraw_area = 0.0
    popumax_area = 0.0
    popu2_area = 0.0
    popu5_area = 0.0
    popu8_area = 0.0
    popu_area = 0.0
    popu_scale_area = 0.0
    fre_area = 0.0
    with open(path.event_dir + 'popularity_' + path.data_name + '.json', 'r') as content:
        for line in content:
            json_line = json.loads(line)
            popuraw_area += float(json_line['popuraw'])
            popumax_area += float(json_line['popumax'])
            popu2_area += float(json_line['popu2'])
            popu5_area += float(json_line['popu5'])
            popu8_area += float(json_line['popu8'])
            popu_area += float(json_line['popu'])
            popu_scale_area += float(json_line['popu_scale'])
            fre_area += float(json_line['fre'])
    content.close()

    with open(path.event_dir + 'popularityNorm_' + path.data_name + '.json', mode='w+') as output:
        with open(path.event_dir + 'popularity_' + path.data_name + '.json', 'r') as content:
            for line in content:
                json_line = json.loads(line)
                line2write = {'date': json_line['date'],
                              'fre': json_line['fre'],
                              'fre_norm': str(float(json_line['fre'])/fre_area),
                              'popuraw': json_line['popuraw'],
                              'popuraw_norm': str(float(json_line['popuraw'])/popuraw_area),
                              'popumax': json_line['popumax'],
                              'popumax_norm': str(float(json_line['popumax'])/popumax_area),
                              'popu2': json_line['popu2'],
                              'popu2_norm': str(float(json_line['popu2'])/popu2_area),
                              'popu5': json_line['popu5'],
                              'popu5_norm': str(float(json_line['popu5'])/popu5_area),
                              'popu8': json_line['popu8'],
                              'popu8_norm': str(float(json_line['popu8'])/popu8_area),
                              'popu': json_line['popu'],
                              'popu_norm': str(float(json_line['popu'])/popu_area),
                              'popu_scale': json_line['popu_scale'],
                              'popu_scale_norm': str(float(json_line['popu_scale'])/popu_scale_area)}
                output.write('{}\n'.format(json.dumps(line2write, ensure_ascii=False)))
        content.close()
    output.close()


def chart_format():
    chart_output = open(path.event_dir + 'chart_' + path.data_name + '.json', 'w+')
    date = ""
    popu = ""
    popu_norm = ""
    popu_scale = ""
    popu_scale_norm = ""
    popuraw = ""
    popuraw_norm = ""
    popumax = ""
    popumax_norm = ""
    popu2 = ""
    popu2_norm = ""
    popu5 = ""
    popu5_norm = ""
    popu8 = ""
    popu8_norm = ""
    fre = ""
    fre_norm = ""
    with open(path.event_dir + 'popularityNorm_' + path.data_name + '.json', 'r') as content:
        for line in content:
            json_line = json.loads(line)
            if date != "":
                date += ","
            date += ('\''+json_line['date']+'\'')
            if popu != "":
                popu += ","
            popu += json_line['popu']
            if fre != "":
                fre += ","
            fre += json_line['fre']
            if fre_norm != "":
                fre_norm += ","
            fre_norm += json_line['fre_norm']
            if popu_norm != "":
                popu_norm += ","
            popu_norm += json_line['popu_norm']
            if popu_scale != "":
                popu_scale += ","
            popu_scale += json_line['popu_scale']
            if popu_scale_norm != "":
                popu_scale_norm += ","
            popu_scale_norm += json_line['popu_scale_norm']
            if popuraw != "":
                popuraw += ","
            popuraw += json_line['popuraw']
            if popuraw_norm != "":
                popuraw_norm += ","
            popuraw_norm += json_line['popuraw_norm']
            if popumax_norm != "":
                popumax_norm += ","
            popumax_norm += json_line['popumax_norm']
            if popumax != "":
                popumax += ","
            popumax += json_line['popumax']
            if popu2 != "":
                popu2 += ","
            popu2 += json_line['popu2']
            if popu5 != "":
                popu5 += ","
            popu5 += json_line['popu5']
            if popu8 != "":
                popu8 += ","
            popu8 += json_line['popu8']
            if popu2_norm != "":
                popu2_norm += ","
            popu2_norm += json_line['popu2_norm']
            if popu5_norm != "":
                popu5_norm += ","
            popu5_norm += json_line['popu5_norm']
            if popu8_norm != "":
                popu8_norm += ","
            popu8_norm += json_line['popu8_norm']
    content.close()
    chart_output.write('date:\n[' + date + ']\n' +
                       'popu:\n[' + popu + ']\n' +
                       'popu_norm:\n[' + popu_norm + ']\n' +
                       'popuraw:\n[' + popuraw + ']\n' +
                       'popuraw_norm:\n[' + popuraw_norm + ']\n' +
                       'popumax:\n[' + popumax + ']\n' +
                       'popumax_norm:\n[' + popumax_norm + ']\n' +
                       'popu2:\n[' + popu2 + ']\n' +
                       'popu2_norm:\n[' + popu2_norm + ']\n' +
                       'popu5:\n[' + popu5 + ']\n' +
                       'popu5_norm:\n[' + popu5_norm + ']\n' +
                       'popu8:\n[' + popu8 + ']\n' +
                       'popu8_norm:\n[' + popu8_norm + ']\n' +
                       'popu_scale:\n[' + popu_scale + ']\n' +
                       'popu_scale_norm:\n[' + popu_scale_norm + ']\n' +
                       'fre:\n[' + fre + ']\n' +
                       'fre_norm:\n[' + fre_norm + ']\n')
    chart_output.close()


if __name__ == '__main__':
    pop_accu()
    pop_norm()
    chart_format()




