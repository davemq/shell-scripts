#!/usr/bin/env python

from collections import defaultdict
import csv
import random
import sys

days = ('Starting City', 'Sunday', 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
starts = []
adjacencies = defaultdict(list)

with open('/home/davemarq/Downloads/ragbrai-by-year.csv', newline='') as csvfile:
    reader= csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        starts.append(row['Starting City'])

with open('/home/davemarq/Downloads/ragbrai-by-year.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = False
    for row in reader:
        if not header:
            header = row
        else:
            for i in range(5,11):
                adjacencies[row[i]].append(row[i+1])

route = []
cur = random.choice(starts)
route.append(cur)
for i in range(7):
    print(adjacencies[cur])
    try:
        next = random.choice(adjacencies[cur])
    except IndexError:
        print("failed!")
        sys.exit(1)
    route.append(next)
    cur = next

print(route)
