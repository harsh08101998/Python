count=1
with open('indeed11_update_allocation.txt  as f:
    lines = f.readlines()
    for i in lines:
        if len(i.strip()) > 0:
            words = i.split('  
            # print(words)
            print(','.join(words), end=" ")
