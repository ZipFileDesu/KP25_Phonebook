import numpy as np
import csv
import pandas as pd

while True:
    print('Input file name:')
    file_name = input();
    try:
        file_in = pd.read_csv(file_name, sep=';', skiprows=0)
    except FileNotFoundError:
        print('Error! File not found. \n')
        continue
    break

positions = set(file_in["Должность"].get_values())
#file_in.close()

with open(file_name.replace(".csv", " Parsed Positions.csv", 1), 'w', encoding="utf-8") as file_out:
    file_out.write("POSITION_NAME \n")
    i = 0
    for pos_name in positions:
        i += 1
        file_out.write(str(i) + ";" + str(pos_name + "\n" if (str(pos_name) != 'nan') else "\n"))