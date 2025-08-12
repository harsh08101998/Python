import pandas as pd
   
# read csv data
df1 = pd.read_excel('hhh2.xlsx 
df2 = pd.read_excel('hhh1.xlsx 

Left_join = pd.merge(df1, 
                     df2, 
                     on ='App_Name', 
                     how ='left 
print(Left_join)