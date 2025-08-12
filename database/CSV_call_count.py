import csv,decimal

# with

lessthen_60=0
greatethen_60=0
with open('478a065a64764feebed931529eadbdd0.csv', 'r  as fr:
    file_reader =csv.DictReader(fr)
    for i in file_reader:
        if int(i['BillableDuration'] )<= 60:
            lessthen_60+=1
        if int(i['BillableDuration']) > 60:
            greatethen_60+=1

print("Call count less then 60 sec :- ", lessthen_60)
print("Call count greater then 60 sec :- ", greatethen_60)




##### For sum price ##############################3
# ss=0
# with open('new1.csv', 'r  as fr:
#     file_reader =csv.DictReader(fr)
#     for i in file_reader:
#         if i['Price']!="":
#             hh=(i['Price'])
#             ss+=decimal.Decimal(hh)

# print(ss)