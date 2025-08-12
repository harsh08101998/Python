import csv,decimal

# with
count=0
ss=0
with open('eeabbbf42288bc824bfe84970f935d07.csv', 'r')  as fr:
    file_reader =csv.DictReader(fr)
    for i in file_reader:
        count+=1
        if i['Price']!="":
            print(i['Price'])
            hh=(i['Price'])
            ss+=decimal.Decimal(hh)
            

print('sum of price :- ',ss)
print('call count :- ',count)