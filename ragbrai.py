#!/usr/bin/env python

import argparse
import csv
import random
from collections import defaultdict
from operator import itemgetter
from pathlib import Path

import graphviz

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
    """Parse CSV file.

    Create
    - starting towns tuple
    - ending towns tuple
    - adjacency lists
    """
    global starts, ends

    with Path.open(
        Path.home() / "shell-scripts/ragbrai-by-year.csv",
        newline="",
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            starts.append(row["Starting City"])
            if row["Saturday"] != "N/A":
                ends.append(row["Saturday"])
            else:
                ends.append(row["Friday"])
    starts = tuple(starts)
    ends = tuple(ends)

    with Path.open(
        Path.home() / "shell-scripts/ragbrai-by-year.csv",
        newline="",
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
    """Create a random route, or None if the created route is invalid."""
    route = []
    cur = random.choice(ends)
    route.append(cur)
    for _ in range(7):
        try:
            nexttown = random.choice(adjacencies[cur])
        except IndexError:
            return None
        route.append(nexttown)
        cur = nexttown
    if cur not in starts:
        return None

    return reversed(route)


def make_graph(name="ragbrai"):
    """Make DOT graph fro adjacencies lists."""
    dot = graphviz.Digraph(name=name, format="png", engine="dot")
    dot.attr(rankdir="LR")

    for s in starts:
        dot.node(s, color="green", shape="tripleoctagon")

    for e in ends:
        dot.node(e, color="red", shape="tripleoctagon")

    for a in adjacencies:
        for node in adjacencies[a]:
            dot.edge(node, a)
    dot = dot.unflatten()
    dot.render(view=True)


args = argparse.ArgumentParser(prog="ragbrai.py", description="Analyze RAGBRAI routes")
args.add_argument("--routes", "-r", default=1000000, help="Number of routes to create")
c = args.parse_args()

parse()
make_graph()

routes = defaultdict(int)

for _ in range(int(c.routes)):
    r = None
    while r is None:
        r = makeroute()
    routes[tuple(r)] += 1
print(f"Created {len(routes)} unique routes")


sortedroutes = dict(sorted(routes.items(), key=itemgetter(1), reverse=True))
for r in sortedroutes:
    print(r, sortedroutes[r])

# Recreate adjacencies from routes[]
adjacencies = defaultdict(set)
starts = set()
ends = set()

for r in routes:
    ends.add(r[-1])
    prev = None
    for town in reversed(r):
        if prev:
            adjacencies[prev].add(town)
        prev = town
    starts.add(prev)

make_graph("generated")
