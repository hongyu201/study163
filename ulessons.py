import os
import csv
from functools import reduce


olessonslist = list()
header = ''
if os.path.exists('lessons.csv'):
    with open('lessons.csv', 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        csv_reader = csv.DictReader(f, fieldnames=header)
        for row in csv_reader:
            dictx = dict()
            for k, v in row.items():
                dictx[k] = v
                olessonslist.append(dictx)

print("未去重前课程数量：{}".format(len(olessonslist)))
ulessonslist = reduce(lambda x, y: x if y in x else x + [y], [[],] + olessonslist)
print("去重后课程数量: {}".format(len(ulessonslist)))


with open('ulessons.csv', 'w', newline='', encoding='UTF-8') as f:
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    for item in ulessonslist:
        writer.writerow(item)
