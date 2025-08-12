import os
import stat
import time, datetime

def get_file_creation_time(file_path):
    # Get the file status using os.stat
    file_stat = os.stat(file_path)
    print(file_stat)
    
    # For Linux, the birth time (creation time) is typically available as file_stat.st_birthtime
    try:
        creation_time = file_stat.st_atime
    except AttributeError:
        # If creation time is not available (on some older file systems), return a message
        return "File creation time not available"

    # Convert the creation time to a readable format
    # return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))
    return datetime.datetime.fromtimestamp(creation_time)

# Example usage:
file_path = 'callreport_harsh.csv'  # Replace with your file path
creation_time = get_file_creation_time(file_path)

print(f"File creation time: {creation_time}")

# print(datetime.datetime.now)
current_time = datetime.datetime.now()

print(current_time)
time_difference = current_time - creation_time
print(time_difference)

if time_difference > datetime.timedelta(minutes=10):
    print( "Error: Time difference is greater than 3 hours")
else:
    print('ok')