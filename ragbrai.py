#!/usr/bin/env python

from collections import defaultdict
import csv
from operator import itemgetter
import random

days = (
    "Starting City",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
)
starts = []
ends = []
adjacencies = defaultdict(list)


def parse():
    global adjacencies, ends, starts

    with open(
        "/home/davemarq/shell-scripts/ragbrai-by-year.csv", newline=""
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            starts.append(row["Starting City"])
            if row["Saturday"] != "N/A":
                ends.append(row["Saturday"])
            else:
                ends.append(row["Friday"])

    with open(
        "/home/davemarq/shell-scripts/ragbrai-by-year.csv", newline=""
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            prev = None
            for d in reversed(days):
                if prev is None:
                    prev = d
                elif row[prev] != "N/A":
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

routes = defaultdict(int)

for i in range(1000000):
    r = None
    while r is None:
        r = makeroute()
    routes[tuple(r)] += 1
print(f"Created {len(routes)} unique routes")

sortedroutes = dict(sorted(routes.items(), key=itemgetter(1), reverse=True))
for r in sortedroutes:
    print(r, sortedroutes[r])
