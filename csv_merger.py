import pandas as pd
  
# reading csv files
a = pd.read_csv('/home/exotel/Pictures/Main_File.csv 
b = pd.read_csv('/home/exotel/Pictures/Total_Completed_Calls.csv 
  
# # using merge function by setting how='left'
# output2 = pd.merge(data1, data2, 
#                    on='Tenant_ID', 
#                    how='left 
  
# # displaying result
# print(output2)
import pandas as pd

# a = pd.read_csv("filea.csv")
# b = pd.read_csv("fileb.csv")
b = b.dropna(axis=1)
merged = a.merge(b, on='Tenant_ID',how='left 
merged.to_csv("kumar.csv", index=False)