from ast import arg
import paramiko
import sys, sys

def run_remote_command(host, username, password, command,port):
    """Run command on remote server and return output"""
    # command = command.split(',') 
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to server
        # print(f"Connecting to {host}...")
        ssh.connect(host, username=username, password=password, timeout=60, port=port)
        
        # Execute command
        print(f"--------- Executing: {command} ---------")
        stdin, stdout, stderr = ssh.exec_command(command, timeout=60)
        
        # Get output
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        exit_status = stdout.channel.recv_exit_status()
        
        # Close connection
        ssh.close()
        
        if exit_status == 0:
            print("✓ Command executed successfully")
            return True, output
        else:
            print(f"✗ Command failed with exit status {exit_status}")
            return False, error if error else output
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        ssh.close()
        return False, str(e)

# Example usage
if __name__ == "__main__":
    host = "192.168.64.3"
    username = "root"
    password = "redhat"
    port = 22


    
    # Example commands
    commands = list(sys.argv[1].split(',')) 
 
    
    for command in commands:
        print(f"\n{'='*50}")
        success, output = run_remote_command(host, username, password, command,port)
        print(f"Output : ------------ \n{output}")