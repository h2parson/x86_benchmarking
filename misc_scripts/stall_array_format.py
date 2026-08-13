stalls = ['3', '3', '2', '9', '4', '4', '5', '6', '6', '4', '4', '6', '5', '3', '2', '6', '5', '4', '5', '6', '4', '7', '6', '5', '4', '3', '4', '10', '5', '4', '5', '5', '4', '6', '5', '5', '5', '3', '4', '6', '3', '5', '6', '4', '4', '7', '5', '4']

stalls_num = [int(s) for s in stalls]

stalls_dict = [{'stalls':n} for n in stalls_num]

import csv

with open('stalls.csv', "w", newline='') as file:
    fieldnames = ['stalls']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(stalls_dict)