import csv
import math

data = []

with open('am_radio_extension.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        data.append(row)
