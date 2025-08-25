import os
import sys
import re
import paramiko
import time

# sudo python3 new_vlan_configs.py centos.pem asterisk 040-veeno-1.exotel.in 22000 bond0 10:192.168.10.123:airtel.sip.com 23:192.168.23.50:jio.sip.com

def usage():
    print(f"Usage: {sys.argv[0]} <ssh-key> <ssh-user> <ssh-host> <ssh-port> <parent-interface> <vlan-id>:<ip-address>:<domain> [<vlan-id>:<ip-address>:<domain> ...]")
    print(f"")
    print(f"IMPORTANT: Use 'root' user or ensure <ssh-user> has full sudo privileges")
    print(f"")
    print(f"Examples:")
    print(f"  {sys.argv[0]} centos.pem root 080-33.exotel.in 22000 bond0 10:192.168.10.123:airtel.sip.com")
    print(f"  {sys.argv[0]} centos.pem asterisk 080-33.exotel.in 22000 bond0 10:192.168.10.123:airtel.sip.com")
    sys.exit(1)

def run_remote_cmd(ssh_client, command):
    """Execute command on remote server with proper privileges"""
    try:
        print(f"$ {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command, timeout=60)
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        rc = stdout.channel.recv_exit_status()
        
        if out:
            print(f"Output: {out}")
        if err and rc != 0:  # Only show errors if command actually failed
            print(f"Error: {err}")
            
        return rc == 0, out, err
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return False, "", str(e)

def create_ssh_connection(key_file, username, hostname, port):
    """Create SSH connection to remote server"""
    if not os.path.exists(key_file):
        print(f"❌ SSH key file not found: {key_file}")
        return None
        
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(key_file)
        ssh.connect(hostname=hostname, username=username, pkey=private_key, port=port, timeout=60)
        print(f"✅ Connected to {username}@{hostname}:{port}")
        
        # Check if we can get root access
        check_root_access(ssh, username)
        return ssh
    except Exception as e:
        print(f"❌ Failed to connect to {hostname}: {e}")
        return None

def check_root_access(ssh_client, username):
    """Check if we have root access or sudo privileges"""
    if username == 'root':
        print("✅ Connected as root user")
        return True
    
    # Test sudo access
    test_cmd = "sudo -n whoami"
    success, out, err = run_remote_cmd(ssh_client, test_cmd)
    
    if success and "root" in out:
        print("✅ Sudo access confirmed")
        return True
    else:
        print("⚠️  Warning: Limited sudo access - some operations may fail")
        return False

def add_to_hosts_file_remote(ssh_client, ip, domain):
    """Add IP and domain to /etc/hosts file on remote server"""
    hosts_file = "/etc/hosts"
    entry = f"{ip}\\t{domain}"
    
    # Check if entry already exists
    success, out, err = run_remote_cmd(ssh_client, f"grep '{domain}' {hosts_file}")
    if success and domain in out:
        print(f"Domain {domain} already exists in {hosts_file}")
        return
    
    # Add new entry
    cmd = f"echo -e '\\n{entry}' | sudo tee -a {hosts_file}"
    success, out, err = run_remote_cmd(ssh_client, cmd)
    
    if success:
        print(f"✅ Added to {hosts_file}: {ip} {domain}")
    else:
        print(f"❌ Failed to update {hosts_file}: {err}")

def update_route_switcher_config_remote(ssh_client, interface_names):
    """Add interface names to route-switcher config file on remote server"""
    config_file = "/home/asterisk/route-switcher/config"
    
    # Read existing config
    success, existing_content, err = run_remote_cmd(ssh_client, f"cat {config_file} 2>/dev/null || echo ''")
    existing_content = existing_content.strip()
    
    if existing_content:
        # Check if it starts with --exclude-interface
        if existing_content.startswith("--exclude-interface "):
            # Extract existing interfaces list
            existing_interfaces_str = existing_content.replace("--exclude-interface ", "")
            existing_interfaces = set(existing_interfaces_str.split(','))
            
            # Add new interfaces
            new_interfaces = set(interface_names)
            all_interfaces = existing_interfaces.union(new_interfaces)
            
            # Create updated config line
            updated_content = f"--exclude-interface {','.join(sorted(all_interfaces))}"
            
            # Check if anything actually changed
            if existing_interfaces == all_interfaces:
                print(f"All interfaces already exist in {config_file}")
                return
        else:
            # Existing content doesn't follow expected format, append to it
            interfaces_str = ",".join(interface_names)
            updated_content = f"{existing_content},--exclude-interface {interfaces_str}"
    else:
        # No existing content, create new
        interfaces_str = ",".join(interface_names)
        updated_content = f"--exclude-interface {interfaces_str}"
    
    # Write updated config
    cmd = f"echo '{updated_content}' > {config_file}"
    success, out, err = run_remote_cmd(ssh_client, cmd)
    
    if success:
        print(f"✅ Updated {config_file}")
        print(f"   Content: {updated_content}")
    else:
        print(f"❌ Failed to update {config_file}: {err}")

def add_iptables_rules_remote(ssh_client, domain, vlan_ip):
    """Add iptables rules for domain and VLAN IP on remote server"""
    
    # Check if domain rule already exists
    check_domain_cmd = f"sudo iptables -L INPUT | grep '{domain}'"
    domain_exists, _, _ = run_remote_cmd(ssh_client, check_domain_cmd)
    
    if not domain_exists:
        cmd1 = f"sudo iptables -A INPUT -s {domain} -j ACCEPT"
        success1, out1, err1 = run_remote_cmd(ssh_client, cmd1)
        if success1:
            print(f"✅ Added iptables rule for domain: {domain}")
        else:
            print(f"❌ Failed to add iptables rule for domain {domain}: {err1}")
    else:
        print(f"✅ Iptables rule for domain {domain} already exists, skipping")
    
    # Check if IP rule already exists
    check_ip_cmd = f"sudo iptables -L INPUT | grep '{vlan_ip}'"
    ip_exists, _, _ = run_remote_cmd(ssh_client, check_ip_cmd)
    
    if not ip_exists:
        cmd2 = f"sudo iptables -A INPUT -s {vlan_ip} -j ACCEPT"
        success2, out2, err2 = run_remote_cmd(ssh_client, cmd2)
        if success2:
            print(f"✅ Added iptables rule for IP: {vlan_ip}")
        else:
            print(f"❌ Failed to add iptables rule for IP {vlan_ip}: {err2}")
    else:
        print(f"✅ Iptables rule for IP {vlan_ip} already exists, skipping")

def save_and_restart_iptables_remote(ssh_client):
    """Save and restart iptables on remote server"""
    
    # Save iptables
    success1, out1, err1 = run_remote_cmd(ssh_client, "sudo service iptables save")
    if success1:
        print("✅ Saved iptables rules")
    else:
        print(f"❌ Failed to save iptables: {err1}")
    
    # Restart iptables
    success2, out2, err2 = run_remote_cmd(ssh_client, "sudo service iptables restart")
    if success2:
        print("✅ Restarted iptables service")
    else:
        print(f"❌ Failed to restart iptables: {err2}")

def read_parent_interface_config(ssh_client, parent_if):
    """Read existing parent interface configuration"""
    cfg_file = f"/etc/sysconfig/network-scripts/{parent_if}"
    
    # Read existing config
    success, content, err = run_remote_cmd(ssh_client, f"sudo cat {cfg_file} 2>/dev/null || echo ''")
    
    if not success or not content.strip():
        print(f"⚠️  Parent interface config {cfg_file} not found, using defaults")
        return {}
    
    print(f"✅ Read parent interface config: {cfg_file}")
    
    # Parse existing configuration into dictionary
    config_dict = {}
    for line in content.strip().split('\n'):
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.split('=', 1)
            config_dict[key.strip()] = value.strip().strip('"').strip("'")
    
    return config_dict

def create_vlan_config_remote(ssh_client, parent_if, vlan_id, ipaddr, gateway_ip, parent_config=None):
    """Create VLAN configuration file based on parent interface config"""
    
    # Extract interface name from filename (remove ifcfg- prefix if present)
    interface_name = parent_if.replace('ifcfg-', '') if parent_if.startswith('ifcfg-') else parent_if
    vlan_if = f"{interface_name}.{vlan_id}"
    cfg_file = f"/etc/sysconfig/network-scripts/ifcfg-{vlan_if}"
    
    # CHECK IF VLAN CONFIG ALREADY EXISTS
    check_cmd = f"sudo test -f {cfg_file}"
    exists, _, _ = run_remote_cmd(ssh_client, check_cmd)
    
    if exists:
        # Check if interface is already up with correct IP
        verify_cmd = f"ip addr show {vlan_if} | grep {ipaddr}"
        ip_exists, ip_out, _ = run_remote_cmd(ssh_client, verify_cmd)
        
        if ip_exists and ipaddr in ip_out:
            print(f"✅ VLAN interface {vlan_if} already exists with IP {ipaddr}, skipping creation")
            return True
        else:
            print(f"⚠️  VLAN config {cfg_file} exists but IP differs, updating...")
    
    # Use provided parent config or read it if not provided (for backward compatibility)
    if parent_config is None:
        parent_config = read_parent_interface_config(ssh_client, parent_if)
    
    # Start with parent config as base
    vlan_config = parent_config.copy()
    
    # ONLY modify these 4 specific parameters - use clean interface name
    vlan_config['DEVICE'] = vlan_if  # This will be "ens256.24" not "ifcfg-ens256.24"
    vlan_config['NAME'] = vlan_if
    vlan_config['IPADDR'] = ipaddr
    vlan_config['GATEWAY'] = gateway_ip
    
    # Build configuration content preserving original format
    config_lines = []
    for key, value in vlan_config.items():
        config_lines.append(f"{key}={value}")
    
    config_content = '\n'.join(config_lines)
    
    print(f"\n📝 VLAN Configuration for {vlan_if}:")
    print("   Modified parameters (only these 4):")
    print(f"     DEVICE={vlan_if}")
    print(f"     NAME={vlan_if}")
    print(f"     IPADDR={ipaddr}")
    print(f"     GATEWAY={gateway_ip}")
    print("   All other settings preserved from parent interface")
    
    # Write config file using tee with sudo
    cmd = f"echo '{config_content}' | sudo tee {cfg_file}"
    success, out, err = run_remote_cmd(ssh_client, cmd)
    
    if success:
        print(f"✅ Created VLAN config: {cfg_file}")
        
        # Set proper permissions
        chmod_cmd = f"sudo chmod 644 {cfg_file}"
        run_remote_cmd(ssh_client, chmod_cmd)
        
        # Load 8021q module if not loaded
        modprobe_cmd = "sudo modprobe 8021q"
        run_remote_cmd(ssh_client, modprobe_cmd)
        
        # Bring up the specific interface
        ifup_cmd = f"nmcli con up {vlan_if}"
        success_ifup, out_ifup, err_ifup = run_remote_cmd(ssh_client, ifup_cmd)
        
        if success_ifup:
            print(f"✅ VLAN interface {vlan_if} brought up successfully")
        else:
            print(f"⚠️  Warning: Failed to bring up VLAN interface {vlan_if}: {err_ifup}")
        
        return True
    else:
        print(f"❌ Failed to create VLAN config {cfg_file}: {err}")
        return False

def calculate_gateway_ip(ip_address):
    """Calculate gateway IP by replacing last octet with 1"""
    octets = ip_address.split('.')
    gateway_ip = f"{octets[0]}.{octets[1]}.{octets[2]}.1"
    return gateway_ip

def calculate_hosts_ip(ip_address):
    """Calculate hosts file IP by replacing last octet with 9"""
    octets = ip_address.split('.')
    hosts_ip = f"{octets[0]}.{octets[1]}.{octets[2]}.9"
    return hosts_ip

def create_backup_directory_remote(ssh_client):
    """Create backup directory on remote server with root privileges"""
    backup_dir = "/tmp/vlan_old_files"
    timestamp = f"_{int(time.time())}"
    backup_dir_with_timestamp = f"{backup_dir}{timestamp}"
    
    cmd = f"sudo mkdir -p {backup_dir_with_timestamp}"
    success, out, err = run_remote_cmd(ssh_client, cmd)
    
    if success:
        # Set proper permissions for asterisk user to read backups if needed
        perm_cmd = f"sudo chmod 755 {backup_dir_with_timestamp}"
        run_remote_cmd(ssh_client, perm_cmd)
        
        print(f"✅ Created backup directory: {backup_dir_with_timestamp}")
        return backup_dir_with_timestamp
    else:
        print(f"❌ Failed to create backup directory: {err}")
        return None

def backup_file_remote(ssh_client, file_path, backup_dir):
    """Backup a file to backup directory on remote server with root privileges"""
    if not file_path or not backup_dir:
        return False
    
    # Get filename from path and add timestamp
    filename = file_path.split('/')[-1]
    timestamp = int(time.time())
    backup_path = f"{backup_dir}/{filename}.backup_{timestamp}"
    
    # Check if file exists before backing up
    check_cmd = f"sudo test -f {file_path}"
    exists, _, _ = run_remote_cmd(ssh_client, check_cmd)
    
    if exists:
        # Copy file to backup directory with root privileges
        backup_cmd = f"sudo cp -p {file_path} {backup_path}"
        success, out, err = run_remote_cmd(ssh_client, backup_cmd)
        
        if success:
            print(f"✅ Backed up: {file_path} → {backup_path}")
            return True
        else:
            print(f"❌ Failed to backup {file_path}: {err}")
            return False
    else:
        print(f"ℹ️  File doesn't exist (will be created): {file_path}")
        return True

def backup_all_files_remote(ssh_client, parent_if, entries):
    """Backup all files that will be modified"""
    print("\n🗄️  CREATING BACKUPS OF EXISTING FILES")
    print("=" * 60)
    
    # Create backup directory
    backup_dir = create_backup_directory_remote(ssh_client)
    if not backup_dir:
        return False
    
    files_to_backup = [
        "/etc/hosts",
        "/home/asterisk/route-switcher/config"
    ]
    
    # Add VLAN config files that might exist
    for entry in entries:
        parts = entry.split(':')
        if len(parts) == 3:
            vlan_id = parts[0]
            if vlan_id.isdigit():
                vlan_if = f"{parent_if}.{vlan_id}"
                cfg_file = f"/etc/sysconfig/network-scripts/ifcfg-{vlan_if}"
                files_to_backup.append(cfg_file)
    
    # Backup each file
    success_count = 0
    for file_path in files_to_backup:
        if backup_file_remote(ssh_client, file_path, backup_dir):
            success_count += 1
    
    # Backup current iptables rules
    iptables_backup = f"{backup_dir}/iptables_rules_backup.txt"
    iptables_cmd = f"sudo iptables-save | sudo tee {iptables_backup} > /dev/null"
    success, out, err = run_remote_cmd(ssh_client, iptables_cmd)
    if success:
        print(f"✅ Backed up iptables rules: {iptables_backup}")
        success_count += 1
    else:
        print(f"❌ Failed to backup iptables rules: {err}")
    
    print(f"\n📋 Backup Summary: {success_count} files backed up successfully")
    print(f"   Backup location: {backup_dir}")
    
    return True

def print_execution_summary(interface_names, hosts_entries, iptables_entries, success_counts, total_attempted):
    """Print detailed summary of all operations"""
    print("\n" + "=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    
    # Show validation results first
    successful_entries = len(interface_names)
    failed_entries = total_attempted - successful_entries
    
    if failed_entries > 0:
        print(f"⚠️  INPUT VALIDATION:")
        print(f"   Total entries: {total_attempted}")
        print(f"   Valid entries: {successful_entries}")
        print(f"   Invalid entries: {failed_entries}")
        print()
    
    total_operations = 0
    successful_operations = 0
    
    # VLAN Interface Summary
    if interface_names:
        total_operations += len(interface_names)
        successful_operations += success_counts.get('vlan_created', 0)
        print(f"VLAN Interfaces: {success_counts.get('vlan_created', 0)}/{len(interface_names)} created")
        for interface in interface_names:
            status = "✅" if interface in success_counts.get('vlan_success_list', []) else "❌"
            print(f"  {status} {interface}")
    
    # Hosts File Summary
    if hosts_entries:
        total_operations += len(hosts_entries)
        successful_operations += success_counts.get('hosts_added', 0)
        print(f"\nHosts Entries: {success_counts.get('hosts_added', 0)}/{len(hosts_entries)} added")
        for hosts_ip, domain in hosts_entries:
            status = "✅" if domain in success_counts.get('hosts_success_list', []) else "❌"
            print(f"  {status} {hosts_ip} → {domain}")
    
    # Route-Switcher Summary
    if success_counts.get('route_switcher_updated'):
        print(f"\n✅ Route-switcher config updated")
        successful_operations += 1
    else:
        print(f"\n❌ Route-switcher config update failed")
    total_operations += 1
    
    # Iptables Summary
    if iptables_entries:
        iptables_success = success_counts.get('iptables_rules_added', 0)
        total_operations += len(iptables_entries) * 2  # domain + IP rules
        successful_operations += iptables_success
        print(f"\nIptables Rules: {iptables_success}/{len(iptables_entries) * 2} added")
        
        if success_counts.get('iptables_saved'):
            print(f"✅ Iptables rules saved and service restarted")
            successful_operations += 1
        else:
            print(f"❌ Failed to save/restart iptables")
        total_operations += 1
    
    # Overall Status
    print("\n" + "=" * 60)
    if successful_operations == total_operations and failed_entries == 0:
        print("🎉 ALL CONFIGURATIONS COMPLETED SUCCESSFULLY!")
    elif successful_operations > 0:
        print(f"⚠️  PARTIAL SUCCESS: {successful_operations}/{total_operations} operations completed")
        if failed_entries > 0:
            print(f"   Note: {failed_entries} entries had invalid format")
    else:
        print("❌ CONFIGURATION FAILED: No operations completed successfully")
    
    print(f"Success Rate: {(successful_operations/total_operations)*100:.1f}%")
    print("=" * 60)

def check_previous_execution(ssh_client, entries, parent_if):
    """Check if script was already run with same parameters"""
    all_exist = True
    
    for entry in entries:
        parts = entry.split(':')
        if len(parts) == 3:
            vlan_id, ipaddr, domain = parts
            vlan_if = f"{parent_if}.{vlan_id}"
            
            # Check VLAN interface
            vlan_cmd = f"ip addr show {vlan_if} 2>/dev/null | grep {ipaddr}"
            vlan_exists, _, _ = run_remote_cmd(ssh_client, vlan_cmd)
            
            # Check hosts entry
            hosts_cmd = f"grep '{domain}' /etc/hosts"
            hosts_exists, _, _ = run_remote_cmd(ssh_client, hosts_cmd)
            
            if not (vlan_exists and hosts_exists):
                all_exist = False
                break
    
    if all_exist:
        print("⚠️  All configurations appear to already exist!")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Exiting...")
            return False
    
    return True

def print_final_verification(ssh_client, interface_names, parent_if):
    """Print final state of all modified files for verification"""
    print("\n" + "🔍 FINAL VERIFICATION - Current State of Modified Files")
    print("=" * 70)
    
    # Helper function to run command and get output without printing command details
    def get_file_content(command):
        try:
            stdin, stdout, stderr = ssh_client.exec_command(command, timeout=60)
            out = stdout.read().decode('utf-8').strip()
            err = stderr.read().decode('utf-8').strip()
            rc = stdout.channel.recv_exit_status()
            return rc == 0, out, err
        except Exception as e:
            return False, "", str(e)
    
    # 1. Show /etc/hosts file
    print("\n1. /etc/hosts file:")
    print("-" * 30)
    success, out, err = get_file_content("cat /etc/hosts")
    if success:
        print(out)
    else:
        print(f"❌ Failed to read /etc/hosts: {err}")
    
    # 2. Show route-switcher config
    print("\n2. Route-switcher configuration:")
    print("-" * 35)
    success, out, err = get_file_content("cat /home/asterisk/route-switcher/config")
    if success:
        print(out)
    else:
        print(f"❌ Failed to read route-switcher config: {err}")
    
    # 3. Show iptables INPUT rules with line numbers
    print("\n3. iptables INPUT rules:")
    print("-" * 25)
    success, out, err = get_file_content("sudo iptables -L INPUT --line-numbers")
    if success:
        print(out)
    else:
        print(f"❌ Failed to read iptables rules: {err}")
    
    # 4. Show parent interface config
    print(f"\n4. Parent interface config ({parent_if}):")
    print("-" * 40)
    success, out, err = get_file_content(f"cat /etc/sysconfig/network-scripts/{parent_if}")
    if success:
        print(out)
    else:
        print(f"❌ Failed to read parent interface config: {err}")
    
    # 5. Show all VLAN interface configs
    if interface_names:
        print(f"\n5. VLAN interface configurations:")
        print("-" * 35)
        for vlan_if in interface_names:
            cfg_file = f"/etc/sysconfig/network-scripts/ifcfg-{vlan_if}"
            print(f"\n📄 {cfg_file}:")
            success, out, err = get_file_content(f"cat {cfg_file}")
            if success:
                print(out)
            else:
                print(f"❌ Failed to read {cfg_file}: {err}")
    
    # 6. Show VLAN interface status
    if interface_names:
        print(f"\n6. VLAN interface status:")
        print("-" * 25)
        for vlan_if in interface_names:
            print(f"\n🔌 {vlan_if} status:")
            success, out, err = get_file_content(f"ip addr show {vlan_if}")
            if success:
                print(out)
            else:
                print(f"❌ Interface {vlan_if} not found or down: {err}")
    
    print("\n" + "=" * 70)
    print("🔍 VERIFICATION COMPLETE")
    print("=" * 70)

def main():
    if len(sys.argv) < 6:
        usage()

    key_file = sys.argv[1]
    ssh_user = sys.argv[2]
    ssh_host = sys.argv[3]
    ssh_port = int(sys.argv[4])
    parent_if = sys.argv[5]
    entries = sys.argv[6:]
    
    if not entries:
        usage()
    
    # Create SSH connection
    ssh_client = create_ssh_connection(key_file, ssh_user, ssh_host, ssh_port)
    if not ssh_client:
        sys.exit(1)
    
    try:
        # Check if configurations already exist
        if not check_previous_execution(ssh_client, entries, parent_if):
            return  # Exit if user chooses not to continue
        
        # STEP 1: CREATE BACKUPS FIRST
        if not backup_all_files_remote(ssh_client, parent_if, entries):
            print("❌ Backup failed. Exiting for safety.")
            return
        
        # Lists to collect data for batch operations
        interface_names = []
        hosts_entries = []
        iptables_entries = []

        print(f"\n🔧 PROCESSING VLAN CONFIGURATIONS")
        print(f"Parent interface: {parent_if}")
        print("=" * 60)

        # Read parent interface configuration once at the beginning (using same interface as parent)
        parent_config = read_parent_interface_config(ssh_client, parent_if)
        if not parent_config:
            print("❌ Failed to read base interface configuration. Exiting.")
            return
        
        total_attempted = 0
        for entry in entries:
            # Parse entry: vlan-id:ip-address:domain
            parts = entry.split(':')
            if len(parts) != 3:
                print(f"❌ Invalid input: {entry}. Must be in format vlan-id:ip-address:domain")
                total_attempted += 1
                continue

            vlan_id, ipaddr, domain = parts

            # Validate VLAN ID and IP address
            if not vlan_id.isdigit() or not re.match(r'^\d+\.\d+\.\d+\.\d+$', ipaddr):
                print(f"❌ Invalid input: {entry}. VLAN ID must be numeric and IP must be valid")
                total_attempted += 1
                continue

            # Calculate gateway IP (replace last octet with 1)
            gateway_ip = calculate_gateway_ip(ipaddr)

            # Calculate hosts file IP (replace last octet with 9) 
            hosts_ip = calculate_hosts_ip(ipaddr)

            # Create VLAN interface name using the provided parent interface
            vlan_if = f"{parent_if}.{vlan_id}"

            print(f"\n🔧 Processing VLAN {vlan_id}:")
            print(f"   Interface: {vlan_if}")
            print(f"   IP: {ipaddr}")
            print(f"   Gateway: {gateway_ip}")  # This will be .1
            print(f"   Hosts IP: {hosts_ip}")   # This will be .9
            print(f"   Domain: {domain}")

            # Create VLAN configuration on remote server
            if create_vlan_config_remote(ssh_client, parent_if, vlan_id, ipaddr, gateway_ip, parent_config):
                # Collect data for batch operations
                interface_names.append(vlan_if)
                hosts_entries.append((hosts_ip, domain))  # ← Use hosts_ip (.9) instead of gateway_ip
                iptables_entries.append((domain, ipaddr))
                print("\n" + "-" * 40)  # Add separator line
                total_attempted += 1
            else:
                total_attempted += 1

        print("\n" + "=" * 60)
        print("🔧 PERFORMING ADDITIONAL CONFIGURATIONS")
        print("=" * 60)

        # Update /etc/hosts file
        print("\n1. Updating /etc/hosts file:")
        for hosts_ip, domain in hosts_entries:
            add_to_hosts_file_remote(ssh_client, hosts_ip, domain)

        # Update route-switcher config
        print("\n2. Updating route-switcher config:")
        if interface_names:
            update_route_switcher_config_remote(ssh_client, interface_names)

        # Add iptables rules
        print("\n3. Adding iptables rules:")
        for domain, vlan_ip in iptables_entries:
            add_iptables_rules_remote(ssh_client, domain, vlan_ip)

        # Save and restart iptables (do this once at the end)
        if iptables_entries:
            print("\n4. Saving and restarting iptables:")
            save_and_restart_iptables_remote(ssh_client)

        # Calculate actual success rates
        total_entries = len(entries)  # Total entries attempted
        successful_vlans = len(interface_names)  # Only successfully processed VLANs

        success_counts = {
            'vlan_created': successful_vlans,
            'vlan_success_list': interface_names,
            'hosts_added': successful_vlans,  # Same as successful VLANs
            'hosts_success_list': [domain for _, domain in hosts_entries],
            'route_switcher_updated': successful_vlans > 0,  # Only if we had valid VLANs
            'iptables_rules_added': successful_vlans * 2,  # Only count successful VLANs
            'iptables_saved': successful_vlans > 0  # Only if we had rules to save
        }

        # Print validation summary before final summary
        print(f"\n📊 VALIDATION SUMMARY:")
        print(f"   Total entries provided: {total_entries}")
        print(f"   Valid entries processed: {successful_vlans}")
        print(f"   Invalid/skipped entries: {total_entries - successful_vlans}")

        # At the end, call the improved summary
        print_execution_summary(interface_names, hosts_entries, iptables_entries, success_counts, len(entries))
        
        # Show final verification of all modified files
        print_final_verification(ssh_client, interface_names, parent_if)

    finally:
        ssh_client.close()
        print(f"\n🔌 SSH connection to {ssh_host} closed")

if __name__ == "__main__":
    main()