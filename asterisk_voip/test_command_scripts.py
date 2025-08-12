import os

prod_path="/home/exotel/bumblebee/"
test_path="/home/exotel/test_bumblebee2/"
number=['08047115433','08047365089']
path=test_path

cmd1 = "python3 "+str(path)+"internal/test_env.py harsh.kumar@exotel.com dnd_check call 07988532204  >> output.txt"
print(cmd1)
os.popen(cmd1,cmd_echo)

cmd2 = "python3 "+str(path)+"internal/test_env.py harsh.kumar@exotel.com dnd_check sms 07988532204  >> output.txt"
print(cmd2)
# os.popen(cmd2)

cmd3 = "python3 "+str(path)+"internal/test_env.py harsh.kumar@exotel.com bulkpntovn "+number[1]+ "  >> output.txt"
print(cmd3)
# os.popen(cmd3)
