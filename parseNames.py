import numpy as np
import csv
import pandas as pd

while True:
    print('Input file name:')
    file_name = input();
    try:
        file_in = pd.read_csv(file_name, sep=';', skiprows=1)
    except FileNotFoundError:
        print('Error! File not found. \n')
        continue
    break

full_names = file_in["ФИО"].get_values()
#file_in.close()
full_names_parsed = []
for field in full_names:
    field = field.split()
    field[0], field[1] = field[1], field[0]
    field = ";".join(field)
    full_names_parsed.append(field)
full_names = None

with open(file_name.replace(".csv", " Parsed Names.csv", 1), 'w', encoding="utf-8") as file_out:
    file_out.write("FIRST_NAME;LAST_NAME;MIDDLE_NAME \n")
    for full_name in full_names_parsed:
        file_out.write(str(full_name) + "\n")