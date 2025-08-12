import os

ip_address=['192.168.0.103']
for i in ip_address:
    print(i)
    cmd = "ssh root@{} 'sudo yum update'".format(i)
    # cmd = "sshpass -p 'HK1998@k' ssh root@{} 'sudo yum update'".format(i)

    os.system(cmd)
    print('\n\n 