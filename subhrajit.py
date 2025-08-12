import csv,decimal

# with
ss=0
with open('new1.csv', 'r  as fr:
    file_reader =csv.DictReader(fr)
    for i in file_reader:
        if i['Price']!="":
            hh=(i['Price'])
            ss+=decimal.Decimal(hh)

print(ss)