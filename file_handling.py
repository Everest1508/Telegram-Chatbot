import csv
fl = open("data.csv",'r')
reader = csv.reader(fl)
for i in list(reader):
    if "Name" in i:
        print("hf")