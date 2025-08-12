import csv

with open('udemy.csv','r  as fr:
    file_reader=csv.DictReader(fr)
    for i in file_reader:
        word=i['name'].strip().replace('_','  
        # word=i['name'].strip()
        print(word.strip(),'\b,','\b',i['id'])

# wordd='Aditya_Rawal'

# print(wordd.count('_ )
# print(wordd.split('_ )
# print(wordd.replace('_','  )