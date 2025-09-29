import csv
import random

days = ('Starting City', 'Sunday', 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
towns = dict()
for day in days:
    towns[day] = []

with open('/home/davemarq/Downloads/ragbrai-by-year.csv', newline='') as csvfile:
    reader= csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        for day in days:
            towns[day].append(row[day])

print(towns)
print(total)
print('Random choice: ')
for day in days:
    print(random.choice(towns[day]))

