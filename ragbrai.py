#!/usr/bin/env python

from collections import defaultdict
import csv
import random
import sys

days = ('Starting City', 'Sunday', 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
starts = []
adjacencies = defaultdict(list)

def parse():
    global adjacencies, starts
    
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
    

def makeroute():
    global adjacencies, starts

    route = []
    cur = random.choice(starts)
    route.append(cur)
    for i in range(7):
        try:
            next = random.choice(adjacencies[cur])
        except IndexError:
            return None
        route.append(next)
        cur = next

    return route


parse()

routes = defaultdict(int)

for i in range(1000000):
    r = None
    while r is None:
        r = makeroute()
    routes[tuple(r)] += 1
print(f"Generated {len(routes)} routes")

sorted = dict(sorted(routes.items(), key=lambda item: item[1], reverse=True))
for r in sorted:
    if sorted[r] < 1000:
        break
    print(r, sorted[r])

