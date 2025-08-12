import os

def call_script_with_argument(argument):
    # Prepare the command string with the argument
    command = f"python3 script1.py {argument}"
    
    # Open the command with os.popen() and capture the output
    with os.popen(command) as pipe:
        output = pipe.read()
    
    return output

# Example usage
parameter = "HelloFromCaller"
output = call_script_with_argument(parameter)
print(f"Output from script1.py: {output}")
