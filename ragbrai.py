#!/usr/bin/env python

from collections import defaultdict
import csv
import random
import sys

days = ('Starting City', 'Sunday', 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
starts = []
ends = []
adjacencies = defaultdict(list)

def parse():
    global adjacencies, ends, starts
    
    with open('/home/davemarq/shell-scripts/ragbrai-by-year.csv', newline='') as csvfile:
        reader= csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            starts.append(row['Starting City'])
            if row['Saturday'] != 'N/A':
                ends.append(row['Saturday'])
            else:
                ends.append(row['Friday'])

    with open('/home/davemarq/shell-scripts/ragbrai-by-year.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        header = False
        for row in reader:
            prev = None
            for d in reversed(days):
                if prev is None:
                    prev = d
                elif row[prev] != 'N/A':
                    adjacencies[row[prev]].append(row[d])
                prev = d
    

def makeroute():
    global adjacencies, ends, starts

    route = []
    cur = random.choice(ends)
    route.append(cur)
    for i in range(7):
        try:
            next = random.choice(adjacencies[cur])
        except IndexError:
            return None
        route.append(next)
        cur = next
    if cur not in starts:
        return None

    return reversed(route)


parse()
# print(f"{len(set(starts))=}")
# print(f"{len(set(ends))=}")
# print(f"{ends=}")

routes = defaultdict(int)

for i in range(1000000):
    r = None
    while r is None:
        r = makeroute()
    routes[tuple(r)] += 1
print(f"Created {len(routes)} unique routes")

sortedroutes = dict(sorted(routes.items(), key=lambda item: item[1], reverse=True))
for r in sortedroutes:
#    if sorted[r] < 2:
#        break
    print(r, sortedroutes[r])

# analyze distribution
# firsts = defaultdict(int)
# lasts = defaultdict(int)
# for r in sortedroutes:
#     firsts[list(r)[0]] += sortedroutes[r]
#     lasts[list(r)[7]] += sortedroutes[r]

# print(f"{len(firsts)=}")
# print(f"{len(lasts)=}")

# print(f"{firsts=}")
# print(f"{lasts=}")

# sortedfirsts = dict(sorted(firsts.items(), key=lambda item: item[1], reverse=True))
# print("sorted firsts:")
# for f in sortedfirsts:
#     print(f, sortedfirsts[f])

# sortedlasts = dict(sorted(lasts.items(), key=lambda item: item[1], reverse=True))
# print("sorted lasts:")
# for l in sortedlasts:
#     print(l, sortedlasts[l])
