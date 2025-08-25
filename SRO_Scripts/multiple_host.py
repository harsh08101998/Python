#!/usr/bin/env python3

import sys
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# python3 multi_host_executor.py centos.pem asterisk 22000 "ls -la /etc/hosts" "080-33.exotel.in,080-34.exotel.in"

def usage():
    print(f"Usage: {sys.argv[0]} <ssh-key> <ssh-user> <ssh-port> <command> <hostnames>")
    print(f"")
    print(f"Where <hostnames> is a comma-separated list of hostnames")
    print(f"")
    print(f"Examples:")
    print(f"  {sys.argv[0]} centos.pem asterisk 22000 'ls -la /etc/hosts' '080-33.exotel.in,080-34.exotel.in'")
    print(f"  {sys.argv[0]} centos.pem root 22000 'systemctl status squid' 'server1.com,server2.com,server3.com'")
    print(f"  {sys.argv[0]} centos.pem asterisk 22000 'df -h' 'host1,host2,host3,host4'")
    print(f"")
    print(f"Note: Use quotes around commands with spaces or special characters")
    print(f"Note: Use quotes around hostname list if it contains spaces")
    sys.exit(1)

def execute_command_on_host(hostname, ssh_user, ssh_key, ssh_port, command, timeout=60):
    """Execute command on a single host using system SSH"""
    result = {
        'hostname': hostname,
        'success': False,
        'output': '',
        'error': '',
        'connection_error': '',
        'execution_time': 0
    }
    
    start_time = time.time()
    
    try:
        # Build SSH command using system ssh (same as your working command)
        ssh_cmd = [
            'ssh',
            '-i', ssh_key,
            '-p', str(ssh_port),
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null',
            '-o', 'ConnectTimeout=30',
            '-o', 'ServerAliveInterval=10',
            '-o', 'ServerAliveCountMax=3',
            f'{ssh_user}@{hostname}',
            command
        ]
        
        # Execute SSH command (Python 3.5+ compatible)
        process = subprocess.Popen(
            ssh_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Handle timeout manually for older Python versions
        try:
            if hasattr(process, 'communicate'):
                # Try with timeout if available (Python 3.3+)
                try:
                    stdout, stderr = process.communicate(timeout=timeout)
                except TypeError:
                    # Fallback for very old Python versions without timeout
                    stdout, stderr = process.communicate()
            else:
                stdout, stderr = process.communicate()
        except Exception:
            process.kill()
            result['connection_error'] = f"Command timed out after {timeout} seconds"
            result['execution_time'] = time.time() - start_time
            return result
        
        result['success'] = process.returncode == 0
        result['output'] = stdout.strip() if stdout else ''
        result['error'] = stderr.strip() if stderr else ''
        result['exit_code'] = process.returncode
        result['execution_time'] = time.time() - start_time
        
        if not result['success'] and result['error']:
            result['connection_error'] = result['error']
        elif not result['success']:
            result['connection_error'] = f"Command failed with exit code {process.returncode}"
            
    except Exception as e:
        result['connection_error'] = f"Unexpected error: {e}"
    
    result['execution_time'] = time.time() - start_time
    return result

def print_host_result(result):
    """Print results for a single host"""
    hostname = result['hostname']
    
    print(f"\n{'='*60}")
    print(f"🖥️  HOST: {hostname}")
    # print(f"{'='*60}")
    
    if result['success']:
        print(f"✅ Connection: SUCCESS")
        print(f"🔄 Exit code: {result.get('exit_code', 'N/A')}")
        
        if result['output']:
            print(f"\n📤 OUTPUT:")
            print("-" * 30)
            print(result['output'])
        else:
            print(f"\n📤 OUTPUT: (empty)")
            
        if result['error']:
            print(f"\n⚠️  STDERR:")
            print("-" * 30)
            print(result['error'])
    else:
        print(f"❌ Connection: FAILED")
        print(f"💥 Error: {result['connection_error']}")

def print_summary(results, command):
    """Print execution summary"""
    total_hosts = len(results)
    successful_hosts = sum(1 for r in results if r['success'])
    failed_hosts = total_hosts - successful_hosts
    
    successful_hostnames = [r['hostname'] for r in results if r['success']]
    failed_hostnames = [r['hostname'] for r in results if not r['success']]
    
    avg_execution_time = sum(r['execution_time'] for r in results if r['success']) / max(successful_hosts, 1)
    
    print(f"\n{'='*70}")
    print(f"📊 EXECUTION SUMMARY")
    print(f"{'='*70}")
    print(f"Command executed: {command}")
    print(f"Total hosts: {total_hosts}")
    print(f"✅ Successful: {successful_hosts}")
    print(f"❌ Failed: {failed_hosts}")
    print(f"📈 Success rate: {(successful_hosts/total_hosts)*100:.1f}%")
    
    
    if successful_hostnames:
        print(f"\n✅ SUCCESSFUL HOSTS ({successful_hosts}):")
        for hostname in successful_hostnames:
            print(f"   • {hostname}")
    
    if failed_hostnames:
        print(f"\n❌ FAILED HOSTS ({failed_hosts}):")
        for hostname in failed_hostnames:
            error = next(r['connection_error'] for r in results if r['hostname'] == hostname)
            print(f"   • {hostname} - {error}")
    
    print(f"{'='*70}")

def validate_ssh_key(ssh_key_path):
    """Validate SSH key file and show key information"""
    if not os.path.exists(ssh_key_path):
        print(f"❌ SSH key file not found: {ssh_key_path}")
        return False
    
    # Check file permissions
    file_stat = os.stat(ssh_key_path)
    file_perms = oct(file_stat.st_mode)[-3:]
    
    if file_perms not in ['600', '400']:
        print(f"⚠️  Warning: SSH key permissions are {file_perms}, should be 600 or 400")
        print(f"   Fix with: chmod 600 {ssh_key_path}")
    
    # Test key with ssh-keygen (most compatible method)
    try:
        test_cmd = ['ssh-keygen', '-l', '-f', ssh_key_path]
        process = subprocess.Popen(
            test_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate(timeout=10)
        
        if process.returncode == 0:
            key_info = stdout.strip()
            print(f"🔑 SSH Key validated: {ssh_key_path}")
            print(f"   Info: {key_info}")
            print(f"   Permissions: {file_perms}")
        else:
            print(f"⚠️  SSH key validation failed: {stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not validate SSH key: {e}")
        return False
    
    return True

def test_ssh_connectivity(ssh_key, ssh_user, ssh_port, hostname):
    """Test SSH connectivity to a single host"""
    print(f"🧪 Testing SSH connectivity to {hostname}...")
    
    ssh_cmd = [
        'ssh',
        '-i', ssh_key,
        '-p', str(ssh_port),
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'ConnectTimeout=10',
        '-o', 'BatchMode=yes',  # Don't prompt for passwords
        f'{ssh_user}@{hostname}'
    ]
    
    try:
        process = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=10)
        if process.returncode == 0:
            print(f"✅ SSH connectivity successful to {hostname}")
            return True
        else:
            print(f"❌ SSH connectivity failed to {hostname}: {process.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ SSH connectivity timed out to {hostname}")
        return False
    except Exception as e:
        print(f"❌ SSH connectivity failed to {hostname}: {e}")
        return False

def main():
    if len(sys.argv) != 6:
        usage()
    
    ssh_key = sys.argv[1]
    ssh_user = sys.argv[2]
    ssh_port = int(sys.argv[3])
    command = sys.argv[4]
    hostnames_str = sys.argv[5]
    
    # Parse comma-separated hostnames
    hostnames = [hostname.strip() for hostname in hostnames_str.split(',') if hostname.strip()]
    
    if not hostnames:
        print("❌ No valid hostnames provided")
        usage()
    
    # Simple SSH key existence check (skip validation)
    if not os.path.exists(ssh_key):
        print(f"❌ SSH key file not found: {ssh_key}")
        sys.exit(1)
    
    print(f"🚀 MULTI-HOST COMMAND EXECUTION")
    print(f"{'='*50}")
    print(f"SSH Key: {ssh_key}")
    print(f"SSH User: {ssh_user}")
    print(f"SSH Port: {ssh_port}")
    print(f"Command: {command}")
    print(f"Total hosts: {len(hostnames)}")
    print(f"Hosts: {', '.join(hostnames)}")
    print(f"{'='*50}")
    
    # Execute commands in parallel using ThreadPoolExecutor
    results = []
    max_workers = min(10, len(hostnames))  # Limit concurrent connections
    
    print(f"\n🔄 Executing command on {len(hostnames)} hosts (max {max_workers} parallel connections)...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_hostname = {
            executor.submit(
                execute_command_on_host, 
                hostname, ssh_user, ssh_key, ssh_port, command
            ): hostname 
            for hostname in hostnames
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_hostname):
            hostname = future_to_hostname[future]
            try:
                result = future.result()
                results.append(result)
                
                # Print progress
                status = "✅" if result['success'] else "❌"
                print(f"{status} {hostname} ({len(results)}/{len(hostnames)})")
                
            except Exception as e:
                print(f"❌ {hostname} - Unexpected error: {e}")
                results.append({
                    'hostname': hostname,
                    'success': False,
                    'output': '',
                    'error': '',
                    'connection_error': f"Unexpected error: {e}",
                    'execution_time': 0
                })
    
    # Sort results by hostname for consistent output
    results.sort(key=lambda x: x['hostname'])
    
    # Print detailed results for each host
    print(f"\n🔍 DETAILED RESULTS")
    for result in results:
        print_host_result(result)
    
    # Print summary
    print_summary(results, command)

if __name__ == "__main__":
    main()