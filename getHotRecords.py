# ===================================================== #
# Get the records of highest popularities in the period #
# ===================================================== #


import json
import path
import os
import re


def get_record():
    source_data = []
    with open(path.afterProcess_path, mode='r') as content:
        for line in content:
            data = json.loads(line)
            source_data.append(data)
    content.close()

    for file_name in os.listdir(path.path_data_dir):
        hot_words = dict()
        with open(path.path_data_dir + file_name) as content:
            for line in content:
                json_line = json.loads(line)
                hot_words[json_line['keyword']] = float(json_line['num']) * float(json_line['factor'])
        content.close()
        date = re.findall('[0-9]+', str(file_name))[0]

        data = []
        for item in source_data:
            if item['create_time'][0:8] == date:
                tmp_popu = 0.0
                word_cnt = 0.0
                for word in item['cut_text']:
                    if word in hot_words:
                        word_cnt += 1
                        tmp_popu += hot_words[word]
                if word_cnt != 0.0:
                    data.append((item, tmp_popu/word_cnt)) 
        if len(data) == 0:
            return

        data = sorted(data, key=lambda d: d[1], reverse=True)

        with open(path.record_dir + 'records-' + path.data_name + '-' + date + '.txt', 'w+') as output_file:
            for i in range(min(100, len(data))):
                output_file.write(data[i][0]['create_time'] + ', ' + str(data[i][1]) + ', ')
                for word in data[i][0]['cut_text']:
                    output_file.write(' ' + word.encode('utf-8'))
                output_file.write('\n')
        output_file.close()


if __name__ == '__main__':
    get_record()
