listt=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
count=0
start=0
end=4
print(round(len(listt)/4))
for i in range(0,4):
    count=0
    slice=listt[start:end]
    for i in slice:
        print(i)
        count+=1
        if count==4:
            start=end
            end+=4