import numpy as np
import csv
import pandas as pd

while True:
    print('Input file name:')
    file_name = "TelPhone.csv"
    try:
        file_in = pd.read_csv(file_name, sep=';', skiprows=1)
    except FileNotFoundError:
        print('Error! File not found. \n')
        continue
    break

parse = list(zip(file_in["ФИО"].get_values(), file_in["Должность"].get_values()))
#file_in.close()

with open(file_name.replace(".csv", " Parsed Names By Position.csv", 1), 'w', encoding="utf-8") as file_out:
    print('Input position_id:')
    id = input()
    print('Input position name:')
    pos_name = input()
    file_out.write("UPDATE public.phonebook_person SET position_id = " + str(id) + " WHERE ")
    i = 0
    for name in parse:
        if (name[1] == pos_name):
            if (i != 0):
                file_out.write(" OR ")
            i += 1
            file_out.write(" full_name = ")
            file_out.write("\'" + (name[0]) + "\' \n")