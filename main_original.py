import csv
import math

original_data = []

with open('am_radio_1-1.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        original_data.append(row[0])

width = math.pi/10000

integral_20440 = 0

cosines = {  # calculated by hand
    "a_one": 20440*math.pi,
    "b_one": 20880*math.pi,
    "c_one": 21760*math.pi,
    "a_two": 40440*math.pi,
    "b_two": 40880*math.pi,
    "c_two": 41760*math.pi
}

integrals = {
    "a_one": 0,
    "b_one": 0,
    "c_one": 0,
    "a_two": 0,
    "b_two": 0,
    "c_two": 0
}

for i in range(0, len(original_data)):  # Calculate the integrals
    ft = float(original_data[i])
    # calculate the cosine value at the t value, which is i * width
    for key in integrals:
        cosine = math.cos(cosines[key]*i*width)
        inner_value = ft*cosine
        integrals[key] += width*inner_value


def get_value(key):
    value = integrals[key]/(-math.pi/4)
    return (key + ", " + str(round(value)))


print(get_value("a_one"))
print(get_value("b_one"))
print(get_value("c_one"))
print(get_value("a_two"))
print(get_value("b_two"))
print(get_value("c_two"))
