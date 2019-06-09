import numpy as np
import csv
import pandas as pd

#Открываем исходный файл с сотрудниками
while True:
    print('Input persons file name:')
    file_name = "TelPhone.csv"
    try:
        file_persons_in = pd.read_csv(file_name, sep=';', skiprows=0)
    except FileNotFoundError:
        print('Error! File not found. \n')
        continue
    break

#Открываем исходный файл с должностями
while True:
    print('Input positions file name:')
    file_name = "Positions.csv"
    try:
        file_positions_in = pd.read_csv(file_name, sep=';', skiprows=0)
    except FileNotFoundError:
        print('Error! File not found. \n')
        continue
    break

parse_persons = list(zip(file_persons_in["ФИО"].get_values(), file_persons_in["Должность"].get_values()))
parse_positions = list(zip(file_positions_in["id"].get_values(), file_positions_in["position_name"].get_values()))

'''print('Input position_id:')
id = input()
print('Input position name:')
pos_name = input()'''
for position in parse_positions:
    with open(" Parsed Names By Position_" + str(position[0]) + ".sql", 'w', encoding="utf-8") as file_out:
        file_out.write("UPDATE public.phonebook_person SET position_id = " + str(position[0]) + " WHERE ")
        i = 0
        for name in parse_persons:
            if (name[1] == position[1]):
                if (i != 0):
                    file_out.write(" OR ")
                i += 1
                file_out.write(" full_name = ")
                file_out.write("\'" + (name[0]) + "\' \n")