import csv

# with
with open('iso.csv', 'r  as fr:
    file_reader =csv.DictReader(fr)
    count=0
    for i in file_reader:
        country=i['Name']
        code=i['Code']
        with open('Countrywise_Call_Cost.csv', 'r   as fr2:
            file_reader2=csv.DictReader(fr2)
            for j in file_reader2:
                # if country.lower()==j['Country'].lower().split()[0]:
                # if j['Country'].lower().find(country.lower()):
                wl=len(country)
        
                if country.lower() == j['Country'].lower()[0:wl] or country.lower() == j['Country'].lower()[0:wl-1]:
                    with open('final.csv','a',newline='  as filewrite:
                        file_writer=csv.DictWriter(filewrite,fieldnames=["Country","Country Code","Per Minute Rates in USD","ISO Country"])
                        # file_writer.writeheader()
                        file_writer.writerow({
                            "Country" :  j['Country'],
                            "Country Code"  : j["Country Code"] ,
                            "Per Minute Rates in USD" :j["Per Minute Rates in USD"] ,
                            "ISO Country" : code
                        })
                else :
                    print(j['Country'])
                    count+=1
                    
    
