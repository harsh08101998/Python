from more_itertools import unique_everseen
with open('ff.csv','r  as f, open('ff2.csv','w  as out_file:
    out_file.writelines(unique_everseen(f))