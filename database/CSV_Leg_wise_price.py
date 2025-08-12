import csv,decimal
import math
from ctypes import sizeof

# with
sum=0
sum2=0
sum3=0
count1=0
count2=0
count3=0
ss=0
ss2=0
with open('43e278599367d64645594a02034789b5.csv', 'r')  as fr:
    file_reader =csv.DictReader(fr)
    for i in file_reader:
        count3+=1
        price=i['PriceDetails']
        number=i['ExotelNumber']
        ll=len(price)
        # print(price)
        if ll > 40 and ll < 100:
            duration=price.find('Duration')
            last=price.find(';')
            # print(last)
            # print(price)
            # print(duration)
            conversation=price[int(duration)+9:int(last)-1]
            # print(conversation)
            hh=math.ceil(int(conversation)/60)
            # print(conversation,hh)
            # conversation,':-',hh
            usd=price.find('USD') 
            usd2=price[int(usd)+4:int(usd)+9]
            print('\'',number,'\'',',',usd2,',',hh)
            valuee=hh
            hk=(i['Price'])
            ss+=decimal.Decimal(hk)
            # if float(i['Price']) != float(valuee):
            #     print(i['Price'],',',round(valuee,2))
                
            #     # print("not match")
            # sum3+=decimal.Decimal(valuee)
            # count1+=1
# print(sum3,ss)
# print("count 3 :-", count3)
# love=0

with open('43e278599367d64645594a02034789b5.csv', 'r')  as fr:
    file_reader =csv.DictReader(fr)
    for i in file_reader:
        price=i['PriceDetails']
        number2=i['ExotelNumber']
        ll=len(price)
        # print(price)
        if ll > 100:
            # print(price)
            duration1=price.find('Duration') 
            price2=price[duration1+20:]
            # print(price2)
            duration2=price2.find('Duration') 
            # print(duration1, duration2)
            # print(price)
            last=price.find( ) 
            last2=price2.find( ) 
            # print(last)
            # conversation1=price[63:int(last)-4]
            conversation1=price[int(duration1)+9:int(last)-3]
            # print(conversation1)
            conversation2=price2[(int(duration2)+9):int(last2-3)]
            # print(conversation2)
            hh=math.ceil(int(conversation1)/60)
            hh2=math.ceil(int(conversation2)/60)
            # conversation,':-',hh
            usd=price.find('USD') 
            usd2=price[int(usd)+4:int(usd)+9]
            # print(usd2)
            usd3=price[usd+20:]
            # print(usd3)
            usd4=usd3.find('USD ')
            usd5=usd3[int(usd4)+4:int(usd4)+9]
           
            # print(usd5)
            print('\'',number2,'\'',',',usd2,',',hh)
            print('\'',number2,'\'',',',usd5,',',hh2)

            # valuee=hh*0.16
            # valuee2=hh2*0.16
            # sum+=decimal.Decimal(valuee)
            # sum2+=decimal.Decimal(valuee2)
            # count2+=1
            # hk=(i['Price'])
            
            # ss2+=decimal.Decimal(hk)
            # love+=round((decimal.Decimal(valuee)+decimal.Decimal(valuee2)),2)
            # print(decimal.Decimal(hk),',',round((decimal.Decimal(valuee)+decimal.Decimal(valuee2)),2))

# print(sum)
# print(sum2)

# print(sum+sum2+sum3)






# print(count1+count2)

# print(ss2)
         
# print(ss2, love)


