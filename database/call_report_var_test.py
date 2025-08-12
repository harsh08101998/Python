import subprocess

var = "ls -lhrt callreport_* | tr -s ' ' | cut -d' ' -f6-9 |cut -d'@' -f1 | cut -d'/' -f1,5 | tr -s '/' ' '"
message = subprocess.check_output(var,shell=True).decode()
print(message)


# Run the command 'ls -lhrt callreport_*' and capture its output
result = subprocess.run(['ls', '-lhrt', 'callreport_*'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(result)
# Check if the command ran successfully
if result.returncode == 0:
    # Split the output into lines (each file is on a separate line)
    output_lines = result.stdout.splitlines()

    # Extract the time from the last column (assuming the format is standard)
    for line in output_lines:
        columns = line.split()
        if len(columns) > 5:  # In case there's more than just the file name
            time = " ".join(columns[5:8])  # Typically, the time is in columns 5 to 7 (Month, Day, Time)
            print("File:", columns[-1], "Timestamp:", time)
else:
    print("Error:", result.stderr)
