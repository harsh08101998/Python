with open("truesoft1m.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Modify lines here
lines = [line.replace("|", ",") for line in lines]

with open("truesoft1m2.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)