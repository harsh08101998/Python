#!/usr/bin/env python3
import argparse
import paramiko
import os
import re
# python3.5 okk.py --ssh-host 080-33.exotel.in --ssh-user asterisk --ssh-key centos.pem --ssh-port 22000

def print_note(note):
    print("\n" + "="*80)
    print(note)
    print("="*80 + "\n")

def run_remote_cmd(host, username, key_file_path, command, port=22):
    print("\n$ {}".format(command))
    if not os.path.exists(key_file_path):
        print("❌ ERROR: SSH key file not found: {}".format(key_file_path))
        return False, "", "SSH key file not found", 1
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        private_key = paramiko.RSAKey.from_private_key_file(key_file_path)
        ssh.connect(hostname=host, username=username, pkey=private_key, port=port, timeout=60)
        stdin, stdout, stderr = ssh.exec_command(command, timeout=60)
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        rc = stdout.channel.recv_exit_status()
        ssh.close()
        success = rc == 0
        return success, out.strip(), err.strip(), rc
    except Exception as e:
        print("Exception: {}".format(e))
        return False, "", str(e), 1

def run_twilix_db_queries(ssh_host):
    import mysql.connector
    from prettytable import from_db_cursor

    print_note("Connecting to Twilix MySQL DB and running queries for server code: {}".format(ssh_host))
    try:
        con = mysql.connector.connect(
            # host='10.1.2.202',  #MUM1
            host='10.0.0.65',  #SGP1
            user='postern',
            password='spyonme',
            database='twilix',
            ssl_disabled=True
        )
        my_cursor = con.cursor()

        # Query 1: Server info
        query1 = "select id,location,created,status,storage,region,host,code from Server where host='{}'".format(ssh_host)
        my_cursor.execute(query1)
        mytable1 = from_db_cursor(my_cursor)
        print("Server table for host '{}':".format(ssh_host))
        print(mytable1)

        # Query 2: PRI info
        query2 = "select id,card,span,plan,fcvPlan,pilot,`range`,pipetype,operatorAccountNumber,state,created,isdStatus from Pri where card in (select id from Card where server in (select id from Server where host ='{}')) and state='active' order by span".format(ssh_host)
        my_cursor.execute(query2)
        mytable2 = from_db_cursor(my_cursor)
        print("PRI table for host '{}':".format(ssh_host)) 
        print(mytable2)

        query3="select * from ServerInterface where ServerId in(select id from Server where host='{}');".format(ssh_host)
        my_cursor.execute(query3)
        mytable3 = from_db_cursor(my_cursor)
        print("ServerInterface table for host '{}':".format(ssh_host))
        print(mytable3)

        con.commit()
        con.close()
    except Exception as e:
        print("Exception while querying Twilix DB:", e)

def task_user_verification(args, command_statuses):
    print_note("User Verification: Check if required users are present in /etc/passwd")
    cmd = "cat /etc/passwd"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    required_users = ["asterisk", "exomon", "recotrix"]
    for user in required_users:
        if user in out:
            print(f"✅ User {user} is present")
            command_statuses.append((cmd, True, f"User {user} is present"))
        else:
            print(f"❌ User {user} is missing")
            command_statuses.append((cmd, False, f"User {user} is missing"))

def task_ssh_configs(args, command_statuses):
    print_note("SSH Configs: Check .ssh directories and authorized_keys for asterisk and exomon")
    for user in ["asterisk", "exomon"]:
        cmd = f"sudo ls -la /home/{user}/.ssh"
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        if not success:
            print(f"❌ Failed to check .ssh directory for {user}")
            print(f"Error: {err}")
            command_statuses.append((cmd, False, f"Failed to check .ssh directory for {user}: {err}"))
        elif "No such file or directory" in out or "No such file or directory" in err:
            print(f"❌ .ssh directory missing for {user}")
            command_statuses.append((cmd, False, f".ssh directory missing for {user}"))
        else:
            print(f"✅ .ssh directory exists for {user}")
            print(out)
            command_statuses.append((cmd, True, f".ssh directory exists for {user}"))
    
    # Check for authorized_keys entries
    for key in ["exotel@prod-build-node", "exotel@Cron-Machine2"]:
        cmd = f'grep "{key}" /home/asterisk/.ssh/authorized_keys'
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        if not success:
            print(f"❌ Failed to check authorized_keys for {key}")
            print(f"Error: {err}")
            command_statuses.append((cmd, False, f"Failed to check authorized_keys for {key}: {err}"))
        elif out.strip():
            print(f"✅ {key} found in authorized_keys")
            command_statuses.append((cmd, True, f"{key} found in authorized_keys"))
        else:
            print(f"❌ {key} NOT found in authorized_keys")
            command_statuses.append((cmd, False, f"{key} NOT found in authorized_keys"))

def task_bash_configs(args, command_statuses):
    print_note("Bash Configs: Check for bash config/history files in /home/asterisk/")
    cmd = "sudo ls -la /home/asterisk/"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if not success:
        print("❌ Failed to check bash config files")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"Failed to check bash config files: {err}"))
        return
    
    required_files = [".bashrc", ".bash_profile", ".bash_history", ".bash_logout"]
    for f in required_files:
        if f in out:
            print(f"✅ {f} is present")
            command_statuses.append((cmd, True, f"{f} is present"))
        else:
            print(f"❌ {f} is missing")
            command_statuses.append((cmd, False, f"{f} is missing"))

            # Special note for .bash_history
            if f == ".bash_history":
                print("Note: In CentOS 7, .bash_history may be missing post deployment. To fix, run:")
                print("sudo cp /root/.bash_history /home/asterisk/;sudo chmod 644 /home/asterisk/.bash_history;sudo chown asterisk:asterisk /home/asterisk/.bash_history")

def task_aws_credentials(args, command_statuses):
    print_note("AWS Credentials: Check AWS credentials for asterisk and root")
    cmd = "cat /home/asterisk/.aws/credentials && cat /root/.aws/credentials"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    print(out)
    if "[default]" in out or "[profile" in out:
        print("✅ AWS credentials file(s) found and non-empty")
        command_statuses.append((cmd, True, "AWS credentials file(s) found and non-empty"))
    else:
        print("❌ AWS credentials file(s) missing or empty")
        command_statuses.append((cmd, False, "AWS credentials file(s) missing or empty"))

def task1_check_local_http_ports(args, command_statuses):
    print_note("Task 1: Check local HTTP ports")
    ports = [9100, 9815, 9256]
    for port in ports:
        cmd = f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{port}"
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if out == "200":
            print(f"✅ Port {port} is up (HTTP 200)")
            command_statuses.append((cmd, True, f"Port {port} is up (HTTP 200)"))
        else:
            print(f"❌ Port {port} is not responding (HTTP {out})")
            command_statuses.append((cmd, False, f"Port {port} is not responding (HTTP {out})"))

def task2_check_ip_platform(args, command_statuses):
    print_note("Task 2: Check IP platform and SIP peers")
    # Check SIP peers
    cmd = 'sudo asterisk -rx "sip show peers" | grep pstn.mum1.exotel.com'
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if "pstn.mum1.exotel.com" in out:
        print("✅ pstn.mum1.exotel.com peer is present in SIP peers")
        command_statuses.append((cmd, True, "pstn.mum1.exotel.com peer is present in SIP peers"))
    else:
        print("❌ pstn.mum1.exotel.com peer is NOT present in SIP peers")
        command_statuses.append((cmd, False, "pstn.mum1.exotel.com peer is NOT present in SIP peers"))
    # Check sillyio config
    cmd = "grep -o 'pstn.mum1.exotel.com' /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if out.count("pstn.mum1.exotel.com") == 3:
        print("✅ sillyio.yml contains three entries for pstn.mum1.exotel.com")
        command_statuses.append((cmd, True, "sillyio.yml contains three entries for pstn.mum1.exotel.com"))
    else:
        print("❌ sillyio.yml does not contain three entries for pstn.mum1.exotel.com")
        command_statuses.append((cmd, False, "sillyio.yml does not contain three entries for pstn.mum1.exotel.com"))

def task3_check_active_channel_script(args, command_statuses):
    print_note("Task 3: Check get_active_numbers.sh script")
    cmd = "[ -x /home/asterisk/get_active_numbers.sh ] && echo 'OK' || echo 'Missing or not executable'"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if "OK" in out:
        print("✅ get_active_numbers.sh is present and executable")
        command_statuses.append((cmd, True, "get_active_numbers.sh is present and executable"))
    else:
        print("❌ get_active_numbers.sh is missing or not executable")
        command_statuses.append((cmd, False, "get_active_numbers.sh is missing or not executable"))

def task_verify_sbc_domains_in_hosts(args, command_statuses):
    print_note("Verify all SBC domains from sillyio.yml (ob_channel_threshold) are present in /etc/hosts")
    # 1. Get all lines with ob_channel_threshold from sillyio.yml
    sillyio_cmd = "grep ob_channel_threshold /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, sillyio_out, sillyio_err, sillyio_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, sillyio_cmd, args.ssh_port
    )
    if not sillyio_out.strip():
        print("❌ No ob_channel_threshold lines found in sillyio.yml")
        command_statuses.append((sillyio_cmd, False, "No ob_channel_threshold lines found in sillyio.yml"))
        return

    # 2. Extract all SBC domains (e.g., jio1.sbc.exotel.com) from those lines
    sbc_domains = set(re.findall(r"'([a-zA-Z0-9\.\-]+\.sbc\.exotel\.com)'", sillyio_out))
    if not sbc_domains:
        print("❌ No SBC domains found in ob_channel_threshold lines")
        command_statuses.append((sillyio_cmd, False, "No SBC domains found in ob_channel_threshold lines"))
        return

    print(f"Found SBC domains: {', '.join(sbc_domains)}")

    # 3. Get /etc/hosts content
    hosts_cmd = "cat /etc/hosts"
    success, hosts_out, hosts_err, hosts_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, hosts_cmd, args.ssh_port
    )

    # 4. Check each SBC domain is present in /etc/hosts
    missing = []
    for domain in sbc_domains:
        if domain not in hosts_out:
            print(f"❌ {domain} is missing in /etc/hosts")
            command_statuses.append((hosts_cmd, False, f"{domain} is missing in /etc/hosts"))
            missing.append(domain)
        else:
            print(f"✅ {domain} is present in /etc/hosts")
            command_statuses.append((hosts_cmd, True, f"{domain} is present in /etc/hosts"))

    if missing:
        print("\nThe following SBC domains are missing in /etc/hosts:")
        for domain in missing:
            print(f"  - {domain}")
    else:
        print("✅ All SBC domains are present in /etc/hosts")

def task5_tcp_connection_recovery(args, command_statuses):
    print_note("Task 5: TCP Connection Recovery Configuration")
    cmd = "sudo sysctl net.ipv4.tcp_retries2"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if "net.ipv4.tcp_retries2 = 8" in out:
        print("✅ net.ipv4.tcp_retries2 is set to 8")
        command_statuses.append((cmd, True, "net.ipv4.tcp_retries2 is set to 8"))
    else:
        print("❌ net.ipv4.tcp_retries2 is not set to 8, attempting to set it")
        cmd1 = "echo 'net.ipv4.tcp_retries2 = 8' | sudo tee -a /etc/sysctl.conf"
        cmd2 = "sudo sysctl -p"
        run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd1, args.ssh_port)
        run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd2, args.ssh_port)
        command_statuses.append((cmd, False, "net.ipv4.tcp_retries2 is not set to 8, attempting to set it"))

def task6_beanstalkd_file_limit(args, command_statuses):
    print_note("Task 6: Beanstalkd File Limit")
    cmds = [
        "cat /etc/init/beanstalkd.conf | grep 'ulimit -n 4096'",
        "cat /etc/systemd/system/beanstalkd.service | grep 'LimitNOFILE=4096'",
        "sudo cat /proc/$(/usr/sbin/pidof beanstalkd)/limits | grep 'Max open files'"
    ]
    for cmd in cmds:
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if "4096" in out:
            print("✅ {} shows 4096".format(cmd))
            command_statuses.append((cmd, True, "{} shows 4096".format(cmd)))
        else:
            print("❌ {} does not show 4096".format(cmd))
            command_statuses.append((cmd, False, "{} does not show 4096".format(cmd)))

def task7_check_iptables(args, command_statuses):
    print_note("Task 7: Check iptables rules")
    cmd = "sudo iptables -L -n"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ iptables rules checked successfully")
        print(out)
        command_statuses.append((cmd, True, "Checked iptables rules"))
    else:
        print("❌ Failed to check iptables rules")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"Failed to check iptables rules: {err}"))

def task8_logrotate_configs(args, command_statuses):
    print_note("Task 8: Check logrotate configs")
    services = ["asterisk","beanstalkd","adhearsion","amix","fail2ban","squid","telegraf","vsftpd","firefoot-ts","eventshipper","rsyslog-errors","haproxy","routeswitcher","fangorn"]
    for service in services:
        cmd = "grep -Ei 'rotate|compress|dateext' /etc/logrotate.d/{}".format(service)
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if out:
            print("✅ {} logrotate config contains rotate/compress/dateext".format(service))
            command_statuses.append((cmd, True, "{} logrotate config contains rotate/compress/dateext".format(service)))
        else:
            print("❌ {} logrotate config missing rotate/compress/dateext".format(service))
            command_statuses.append((cmd, False, "{} logrotate config missing rotate/compress/dateext".format(service)))


def task10_squid_status(args, command_statuses):
    print_note("Task 10: Squid status")
    cmds = [
        "sudo service squid status",
        "/usr/sbin/squid -v"
    ]
    for i, cmd in enumerate(cmds):
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        if success:
            print(f"✅ {cmd}")
            print(out)
            command_statuses.append((cmd, True, "Checked Squid status"))
        else:
            print(f"❌ {cmd}")
            print(f"Error: {err}")
            command_statuses.append((cmd, False, f"Squid status check failed: {err}"))

def task11_haproxy_status(args, command_statuses):
    print_note("Task 11: HAProxy status")
    cmds = [
        "sudo service haproxy status",
        "/usr/local/sbin/haproxy -v"
    ]
    for i, cmd in enumerate(cmds):
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        if success:
            print(f"✅ {cmd}")
            print(out)
            command_statuses.append((cmd, True, "Checked HAProxy status"))
        else:
            print(f"❌ {cmd}")
            print(f"Error: {err}")
            command_statuses.append((cmd, False, f"HAProxy status check failed: {err}"))

def task12_check_recording_status(args, command_statuses):
    print_note("Task 12: Verifying recording status in exotelcalls DB")
    cmd = (
        "mysql -uroot -pcell4business exotelcalls "
        "-e \"SELECT COUNT(*), status, DATE(date_created) FROM recordings "
        "GROUP BY status, DATE(date_created) ORDER BY DATE(date_created) LIMIT 5;\""
    )
    success, out, err, rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port
    )
    print(out)
    if success:
        command_statuses.append((cmd, True, "Checked recording status in exotelcalls DB"))
    else:
        command_statuses.append((cmd, False, "Failed to check recording status in exotelcalls DB"))

def task13_check_for_AMI_Events_status(args, command_statuses):
    print_note("Task 13: Verifying AMI events status in ExotelCalls")
    cmd = (
        "mysql -uroot -pcell4business exotelcalls "
        "-e \"select  count(*), eventname, DATE(date_created) from amievent "
        "group by eventname, DATE(date_created) order by DATE(date_created) desc limit 50;\""
    )
    success, out, err, rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port
    )
    print(out)
    if success:
        command_statuses.append((cmd, True, "Checked AMI events status in asteriskStoreDB"))
    else:
        command_statuses.append((cmd, False, "Failed to check AMI events status in asteriskStoreDB"))

def task14_check_asterisk_srtp(args, command_statuses):
    print_note("Check if Asterisk SRTP module is present")
    cmd = '/usr/sbin/asterisk -rx "module show like srtp"'
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    print("STDOUT:", out)
    print("STDERR:", err)
    if "1 modules loaded" in out or "res_srtp.so" in out:
        print("✅ SRTP module is present in Asterisk")
        command_statuses.append((cmd, True, "SRTP module is present in Asterisk"))
    else:
        print("❌ SRTP module is NOT present in Asterisk")
        command_statuses.append((cmd, False, "SRTP module is NOT present in Asterisk"))

def task_check_rsyslog_mum1(args, command_statuses):
    print_note("Check for Mumbai stamp rsyslog server entries in /etc/rsyslog.d/logs.conf")
    cmd = 'grep mum1 /etc/rsyslog.d/logs.conf'
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    print(out)
    expected = 'Target="rsyslog.mum1.exotel.in"'
    count = out.count(expected)
    if count >= 1:
        print(f"✅ Found {count} Mumbai rsyslog server entries in logs.conf")
        command_statuses.append((cmd, True, f"Found {count} Mumbai rsyslog server entries in logs.conf"))
    else:
        print("❌ Mumbai rsyslog server entry not found in logs.conf")
        command_statuses.append((cmd, False, "Mumbai rsyslog server entry not found in logs.conf"))

def task_check_manager_interface_actionid(args, command_statuses):
    print_note('Check for single "aid = headers.delete(:ActionID)" in manager_interface.rb')
    cmd = "grep 'ActionID' /opt/jruby-1.7.1/lib/ruby/gems/shared/gems/adhearsion-1.2.6/lib/adhearsion/voip/asterisk/manager_interface.rb | grep headers.delete"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    count = out.count("aid = headers.delete(:ActionID)")
    if count == 1:
        print("✅ Only one entry of 'aid = headers.delete(:ActionID)' found")
        command_statuses.append((cmd, True, "Only one entry of 'aid = headers.delete(:ActionID)' found"))
    else:
        print(f"❌ {count} entries of 'aid = headers.delete(:ActionID)' found (should be 1)")
        print(out)
        command_statuses.append((cmd, False, f"{count} entries of 'aid = headers.delete(:ActionID)' found (should be 1)"))

def task_check_nproc_value(args, command_statuses):
    print_note("Check nproc value in /etc/security/limits.d/20-nproc.conf (should be 20480)")
    cmd = "grep -E '^[^#]*[0-9]+$' /etc/security/limits.d/20-nproc.conf"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if "20480" in out:
        print("✅ nproc value is set to 20480")
        command_statuses.append((cmd, True, "nproc value is set to 20480"))
    else:
        print("❌ nproc value is NOT set to 20480")
        print(out)
        command_statuses.append((cmd, False, "nproc value is NOT set to 20480"))

def task_check_ahn_timezone(args, command_statuses):
    print_note("Check Ahn time zone in Ahn logs (should be +05:30 or +0530)")
    cmd = "cat /var/log/exotel/ahn_health/adhearsion_dates"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if "+05:30" in out or "+0530" in out:
        print("✅ Ahn log time zone is IST (+05:30 or +0530)")
        command_statuses.append((cmd, True, "Ahn log time zone is IST (+05:30 or +0530)"))
    else:
        print("❌ Ahn log time zone is NOT IST (+05:30 or +0530)")
        print(out)
        command_statuses.append((cmd, False, "Ahn log time zone is NOT IST (+05:30 or +0530)"))

def task9_squid_health_and_proxy_checks(args, command_statuses):
    print_note("Squid/HAProxy Health and Proxy Functionality Checks")
    cmds = [
        "curl -v http://localhost:5000/healthcheck",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23451' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23452' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23432' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23433' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "sudo service haproxy status",
        "sudo service squid status",
        "cat /etc/haproxy/haproxy.cfg"
    ]
    for cmd in cmds:
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        print(f"\nCommand: {cmd}\nSTDOUT:\n{out}\nSTDERR:\n{err}")
        # For curl commands, consider HTTP 200 as success
        if "curl" in cmd:
            if "200 OK" in out or "200 OK" in err or rc == 0:
                print(f"✅ {cmd} succeeded")
                command_statuses.append((cmd, True, f"{cmd} succeeded"))
            else:
                print(f"❌ {cmd} failed")
                command_statuses.append((cmd, False, f"{cmd} failed"))
        else:
            if rc == 0:
                print(f"✅ {cmd} succeeded")
                command_statuses.append((cmd, True, f"{cmd} succeeded"))
            else:
                print(f"❌ {cmd} failed")
                command_statuses.append((cmd, False, f"{cmd} failed"))

def task_verify_route_switcher_config(args, command_statuses):
    print_note("Verifying route-switcher config: all interface names should be present in /home/asterisk/route-switcher/config")
    # 1. Get all interface names except 'lo'
    iface_cmd = "ls /sys/class/net | grep -v '^lo$'"
    success, iface_out, iface_err, iface_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, iface_cmd, args.ssh_port
    )
    if not iface_out.strip():
        print("❌ No network interfaces found (except lo)")
        command_statuses.append((iface_cmd, False, "No network interfaces found (except lo)"))
        return

    interfaces = [line.strip() for line in iface_out.splitlines() if line.strip()]
    print(f"Found interfaces: {', '.join(interfaces)}")

    # 2. Read the route-switcher config file
    config_cmd = "cat /home/asterisk/route-switcher/config"
    success, config_out, config_err, config_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, config_cmd, args.ssh_port
    )
    if not config_out.strip():
        print("❌ route-switcher config file is empty or missing")
        command_statuses.append((config_cmd, False, "route-switcher config file is empty or missing"))
        return

    # 3. Check each interface is present in the config
    missing = []
    for iface in interfaces:
        if iface not in config_out:
            print(f"❌ Interface {iface} is missing in route-switcher config")
            command_statuses.append((config_cmd, False, f"Interface {iface} is missing in route-switcher config"))
            missing.append(iface)
        else:
            print(f"✅ Interface {iface} is present in route-switcher config")
            command_statuses.append((config_cmd, True, f"Interface {iface} is present in route-switcher config"))

    if missing:
        print("\nThe following interfaces are missing in route-switcher config:")
        for iface in missing:
            print(f"  - {iface}")
    else:
        print("✅ All interfaces are present in route-switcher config")

def task_sillyio_config_verification(args, command_statuses):
    print_note("Sillyio config verification: s3_recording_bucket and conference_master")

    # 1. Check s3_recording_bucket
    s3_cmd = "grep s3_recording_bucket /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, s3_out, s3_err, s3_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, s3_cmd, args.ssh_port
    )
    expected_url = "https://s3-ap-southeast-1.amazonaws.com/exotelrecordings/"
    if expected_url in s3_out:
        print(f"✅ s3_recording_bucket is set correctly: {expected_url}")
        command_statuses.append((s3_cmd, True, f"s3_recording_bucket is set correctly: {expected_url}"))
    else:
        print(f"❌ s3_recording_bucket is not set to {expected_url}")
        print(f"Found: {s3_out.strip()}")
        command_statuses.append((s3_cmd, False, f"s3_recording_bucket is not set to {expected_url}. Found: {s3_out.strip()}"))

    # 2. Check conference_master
    conf_cmd = "grep conference_master /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, conf_out, conf_err, conf_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, conf_cmd, args.ssh_port
    )
    if conf_out.strip():
        print("✅ conference_master is present in sillyio config")
        print(conf_out.strip())
        command_statuses.append((conf_cmd, True, "conference_master is present in sillyio config"))
    else:
        print("❌ conference_master is NOT present in sillyio config")
        command_statuses.append((conf_cmd, False, "conference_master is NOT present in sillyio config"))

def task_squid_config_validation(args, command_statuses):
    print_note("Squid Configuration Validation: tcp_outgoing_address vs Ethernet Interfaces")
    
    # 1. Get all ethernet interfaces (em1, em2, em3, em4)
    iface_cmd = "ls /sys/class/net | grep -E '^em[1-4]$'"
    success, iface_out, iface_err, iface_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, iface_cmd, args.ssh_port
    )
    
    if not iface_out.strip():
        print("❌ No ethernet interfaces (em1-em4) found")
        command_statuses.append((iface_cmd, False, "No ethernet interfaces (em1-em4) found"))
        return
    
    ethernet_interfaces = [line.strip() for line in iface_out.splitlines() if line.strip()]
    print(f"Found ethernet interfaces: {', '.join(ethernet_interfaces)}")
    
    # 2. Get IP addresses for each ethernet interface
    interface_ips = {}
    for iface in ethernet_interfaces:
        ip_cmd = f"ip addr show {iface} | grep 'inet ' | awk '{{print $2}}' | cut -d'/' -f1"
        success, ip_out, ip_err, ip_rc = run_remote_cmd(
            args.ssh_host, args.ssh_user, args.ssh_key, ip_cmd, args.ssh_port
        )
        if ip_out.strip():
            interface_ips[iface] = ip_out.strip()
            print(f"✅ {iface}: {ip_out.strip()}")
        else:
            print(f"❌ {iface}: No IP address found")
            command_statuses.append((ip_cmd, False, f"{iface}: No IP address found"))
    
    # 3. Check tcp_outgoing_address in squid.conf
    squid_cmd = "sudo grep tcp_outgoing_address /etc/squid/squid.conf"
    success, squid_out, squid_err, squid_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, squid_cmd, args.ssh_port
    )
    
    if not squid_out.strip():
        print("❌ No tcp_outgoing_address entries found in squid.conf")
        command_statuses.append((squid_cmd, False, "No tcp_outgoing_address entries found in squid.conf"))
        return
    
    print("Squid tcp_outgoing_address entries:")
    print(squid_out)
    
    # 4. Validate that all interface IPs are configured in squid
    configured_ips = set()
    for line in squid_out.splitlines():
        if "tcp_outgoing_address" in line:
            # Extract IP from line like: tcp_outgoing_address 192.168.1.10 ip1
            parts = line.strip().split()
            if len(parts) >= 2:
                configured_ips.add(parts[1])
    
    missing_ips = []
    for iface, ip in interface_ips.items():
        if ip not in configured_ips:
            print(f"❌ {iface} IP ({ip}) is missing in squid tcp_outgoing_address")
            command_statuses.append((squid_cmd, False, f"{iface} IP ({ip}) is missing in squid tcp_outgoing_address"))
            missing_ips.append(f"{iface}:{ip}")
        else:
            print(f"✅ {iface} IP ({ip}) is configured in squid tcp_outgoing_address")
            command_statuses.append((squid_cmd, True, f"{iface} IP ({ip}) is configured in squid tcp_outgoing_address"))
    
    if missing_ips:
        print(f"\nMissing IPs in squid configuration: {', '.join(missing_ips)}")
    else:
        print("✅ All ethernet interface IPs are configured in squid tcp_outgoing_address")

def task_squid_comprehensive_validation(args, command_statuses):
    print_note("Comprehensive Squid Validation: Version, Configuration & Proxy Testing")
    
    # 1. Check Squid version
    version_cmd = "/usr/sbin/squid -v"
    success, version_out, version_err, version_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, version_cmd, args.ssh_port
    )
    expected_version = "3.5.28"
    if expected_version in version_out:
        print(f"✅ Squid version is correct: {expected_version}")
        command_statuses.append((version_cmd, True, f"Squid version is correct: {expected_version}"))
    else:
        print(f"❌ Squid version mismatch. Expected: {expected_version}, Got: {version_out}")
        command_statuses.append((version_cmd, False, f"Squid version mismatch. Expected: {expected_version}, Got: {version_out}"))
    
    # 2. Check Squid service status
    status_cmd = "sudo service squid status"
    success, status_out, status_err, status_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, status_cmd, args.ssh_port
    )
    print(f"Command: {status_cmd}")
    if not success:
        print("❌ Failed to check Squid service status")
        print(f"Error: {status_err}")
        command_statuses.append((status_cmd, False, f"Squid service status check failed: {status_err}"))
        return  # Exit early if SSH fails
    else:
        print(f"Output: {status_out}")
        if "running" in status_out.lower() or "active" in status_out.lower():
            print("✅ Squid service is running")
            command_statuses.append((status_cmd, True, "Squid service is running"))
        else:
            print("❌ Squid service is not running")
            command_statuses.append((status_cmd, False, "Squid service is not running"))
    
    # 3. Enhanced squid configuration validation
    config_validation_cmd = (
        'echo ""; /usr/sbin/squid -v | grep -i "Version"; echo ""; '
        '/usr/local/sbin/haproxy -v | grep -i "Version"; echo ""; '
        'cat /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml | grep -i "proxy_url\\|http://localhost"; echo ""; '
        'cat /etc/haproxy/haproxy.cfg | grep -i "check fall"; echo ""; '
        'sudo cat /etc/squid/squid.conf | grep -i "acl ip\\|tcp_outgoing_ad\\|http_port"'
    )
    success, config_out, config_err, config_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, config_validation_cmd, args.ssh_port
    )
    
    if success:
        print("✅ Squid/HAProxy configuration summary checked successfully")
        print("Squid/HAProxy Configuration Summary:")
        print(config_out)
        command_statuses.append((config_validation_cmd, True, "Checked squid/haproxy configuration summary"))
    else:
        print("❌ Failed to check Squid/HAProxy configuration summary")
        print(f"Error: {config_err}")
        command_statuses.append((config_validation_cmd, False, f"Failed to check squid/haproxy configuration summary: {config_err}"))
    
    # 4. Comprehensive proxy testing - Updated validation logic
    proxy_tests = [
        "curl -v http://localhost:5000/healthcheck",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23451' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23452' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23432' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23433' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'"
    ]
    
    working_responses = 0
    for cmd in proxy_tests:
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        # Updated validation logic for different response types
        is_success = False
        if "healthcheck" in cmd:
            # For healthcheck endpoint, look for success message
            if '"success":true' in out or "All cool here" in out:
                is_success = True
        else:
            # For other proxy tests, look for Working status or HTTP 200
            if '"status": "Working"' in out or "200" in out or rc == 0:
                is_success = True
        
        if is_success:
            print(f"✅ Proxy test succeeded: {cmd[:50]}...")
            command_statuses.append((cmd, True, "Proxy test succeeded"))
            working_responses += 1
        else:
            print(f"❌ Proxy test failed: {cmd[:50]}...")
            print(f"Response: {out[:100]}...")
            command_statuses.append((cmd, False, "Proxy test failed"))
    
    print(f"\nProxy Test Summary: {working_responses}/{len(proxy_tests)} tests passed")
    
    # Expected output validation
    if working_responses >= len(proxy_tests) - 1:  # Allow 1 failure
        print('✅ Expected output: Multiple {"status": "Working"} responses received')
        command_statuses.append(("proxy_summary", True, f"Proxy tests passed: {working_responses}/{len(proxy_tests)}"))
    else:
        print(f'❌ Expected multiple {{"status": "Working"}} responses, got {working_responses}')
        command_statuses.append(("proxy_summary", False, f"Insufficient proxy tests passed: {working_responses}/{len(proxy_tests)}"))

def task_squid_detailed_status_validation(args, command_statuses):
    print_note("Detailed Squid Status Validation (CSV Requirements)")
    
    # Step 1: Check squid service status
    print("Step 1: Checking Squid Service Status")
    status_cmd = "sudo service squid status"
    success, status_out, status_err, status_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, status_cmd, args.ssh_port
    )
    print(f"Command: {status_cmd}")
    print(f"Output: {status_out}")
    if "running" in status_out.lower() or "active" in status_out.lower():
        print("✅ Squid service is running")
        command_statuses.append((status_cmd, True, "Squid service is running"))
    else:
        print("❌ Squid service is not running")
        command_statuses.append((status_cmd, False, "Squid service is not running"))
    
    # Step 2: Check squid version
    print("\nStep 2: Checking Squid Version")
    version_cmd = "/usr/sbin/squid -v"
    success, version_out, version_err, version_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, version_cmd, args.ssh_port
    )
    print(f"Command: {version_cmd}")
    print(f"Output: {version_out}")
    
    expected_version = "Squid Cache: Version 3.5.28"
    if "3.5.28" in version_out:
        print("✅ Squid version is correct: 3.5.28")
        command_statuses.append((version_cmd, True, "Squid version is correct: 3.5.28"))
    else:
        print(f"❌ Squid version mismatch. Expected: 3.5.28, Got: {version_out}")
        command_statuses.append((version_cmd, False, f"Squid version mismatch. Expected: 3.5.28"))
    
    # Step 3: Comprehensive configuration validation command
    print("\nStep 3: Comprehensive Configuration Validation")
    comprehensive_cmd = (
        'echo ""; /usr/sbin/squid -v | grep -i "Version"; echo ""; '
        '/usr/local/sbin/haproxy -v | grep -i "Version"; echo ""; '
        'cat /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml | grep -i "proxy_url\\|http://localhost"; echo ""; '
        'cat /etc/haproxy/haproxy.cfg | grep -i "check fall"; echo ""; '
        'sudo cat /etc/squid/squid.conf | grep -i "acl ip\\|tcp_outgoing_ad\\|http_port"'
    )
    
    success, comprehensive_out, comprehensive_err, comprehensive_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, comprehensive_cmd, args.ssh_port
    )
    
    print("Comprehensive Configuration Output:")
    print("=" * 80)
    print(comprehensive_out)
    print("=" * 80)
    
    # Validate specific components in the output
    validation_checks = [
        ("Squid Version", "3.5.28", "✅ Squid version found in output"),
        ("HAProxy Version", "2.4.2", "✅ HAProxy version found in output"),
        ("Proxy URL", "http://localhost:23432", "✅ Proxy URL configuration found"),
        ("Check Fall Config", "check fall", "✅ HAProxy check fall configuration found"),
        ("ACL IP Config", "acl ip", "✅ Squid ACL IP configuration found"),
        ("TCP Outgoing Address", "tcp_outgoing_address", "✅ TCP outgoing address configuration found"),
        ("HTTP Port Config", "http_port", "✅ HTTP port configuration found")
    ]
    
    passed_checks = []
    failed_checks = []
    
    for check_name, search_term, success_msg in validation_checks:
        if search_term.lower() in comprehensive_out.lower():
            print(success_msg)
            passed_checks.append(check_name)
        else:
            error_msg = f"❌ {check_name} configuration not found"
            print(error_msg)
            failed_checks.append(check_name)
    
    # Record the command only once with summary
    summary = f"Comprehensive validation - Passed: {len(passed_checks)}, Failed: {len(failed_checks)}"
    overall_success = len(failed_checks) == 0
    command_statuses.append((comprehensive_cmd, overall_success, summary))

    # Additional validation for ILL IPs configuration
    print("\nValidating ILL IPs Configuration:")
    
    # Check for expected patterns
    if "acl ip1 myport" in comprehensive_out and "acl ip2 myport" in comprehensive_out:
        print("✅ ACL IP port configurations found")
    else:
        print("❌ ACL IP port configurations missing")
    
    # Count tcp_outgoing_address entries
    tcp_outgoing_count = comprehensive_out.lower().count("tcp_outgoing_address")
    if tcp_outgoing_count >= 3:
        print(f"✅ Found {tcp_outgoing_count} tcp_outgoing_address entries (minimum 3 for 3 ILLs)")
    else:
        print(f"❌ Only found {tcp_outgoing_count} tcp_outgoing_address entries (expected minimum 3)")
    
    # Count http_port entries
    http_port_count = comprehensive_out.lower().count("http_port")
    if http_port_count >= 3:
        print(f"✅ Found {http_port_count} http_port entries (minimum 3 for 3 ILLs)")
    else:
        print(f"❌ Only found {http_port_count} http_port entries (expected minimum 3)")

def task_squid_proxy_working_validation(args, command_statuses):
    print_note("Squid Proxy Working Status Validation (Expected 5 Working Responses)")
    
    # Test commands for 3 ILL configuration (from CSV)
    proxy_test_commands = [
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23451' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23452' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23453' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23432' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23433' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'"
    ]
    
    working_responses = []
    failed_responses = []
    
    for i, cmd in enumerate(proxy_test_commands, 1):
        print(f"\nTesting Proxy {i}/5:")
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        # Check for expected "Working" response
        if '"status": "Working"' in out or "200" in out or '"success":true' in out:
            print(f"✅ Proxy test {i} succeeded - Got 'Working' response")
            working_responses.append(i)
            command_statuses.append((f"proxy_test_{i}", True, f"Proxy test {i} succeeded"))
        else:
            print(f"❌ Proxy test {i} failed - Expected 'Working' response")
            print(f"Response: {out[:200]}...")
            failed_responses.append(i)
            command_statuses.append((f"proxy_test_{i}", False, f"Proxy test {i} failed"))
    
    # Summary validation
    print(f"\n{'='*60}")
    print("PROXY TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Working Responses: {len(working_responses)}/5")
    print(f"Failed Responses: {len(failed_responses)}/5")
    
    # Expected output validation (from CSV: 5 Working responses for 3 ILL setup)
    if len(working_responses) == 5:
        print('✅ SUCCESS: All 5 proxy tests returned {"status": "Working"}')
        print("Expected output achieved:")
        for i in range(5):
            print('{"status": "Working"}')
        command_statuses.append(("proxy_summary", True, "All 5 proxy tests succeeded"))
    elif len(working_responses) >= 3:
        print(f'⚠️  PARTIAL SUCCESS: {len(working_responses)}/5 proxy tests working (minimum 3 for basic functionality)')
        command_statuses.append(("proxy_summary", True, f"Partial success: {len(working_responses)}/5 proxy tests working"))
    else:
        print(f'❌ FAILURE: Only {len(working_responses)}/5 proxy tests working (insufficient for operation)')
        command_statuses.append(("proxy_summary", False, f"Insufficient proxy tests working: {len(working_responses)}/5"))

def task_haproxy_detailed_status_validation(args, command_statuses):
    print_note("Detailed HAProxy Status Validation (CSV Requirements)")
    
    # Step 1: Check HAProxy service status
    print("Step 1: Checking HAProxy Service Status")
    status_cmd = "sudo service haproxy status"
    success, status_out, status_err, status_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, status_cmd, args.ssh_port
    )
    print(f"Command: {status_cmd}")
    if not success:
        print("❌ Failed to check HAProxy service status")
        print(f"Error: {status_err}")
        command_statuses.append((status_cmd, False, f"HAProxy service status check failed: {status_err}"))
        return  # Exit early if SSH fails
    else:
        print(f"Output: {status_out}")
        if "running" in status_out.lower() or "active" in status_out.lower():
            print("✅ HAProxy service is running")
            command_statuses.append((status_cmd, True, "HAProxy service is running"))
        else:
            print("❌ HAProxy service is not running")
            command_statuses.append((status_cmd, False, "HAProxy service is not running"))
    
    # Step 2: Check HAProxy version
    print("\nStep 2: Checking HAProxy Version")
    version_cmd = "/usr/local/sbin/haproxy -v"
    success, version_out, version_err, version_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, version_cmd, args.ssh_port
    )
    print(f"Command: {version_cmd}")
    print(f"Output: {version_out}")
    
    expected_version = "HAProxy version 2.4.2-553dee3 2021/07/07"
    if "2.4.2-553dee3" in version_out and "2021/07/07" in version_out:
        print("✅ HAProxy version is correct: 2.4.2-553dee3 2021/07/07")
        command_statuses.append((version_cmd, True, "HAProxy version is correct: 2.4.2-553dee3 2021/07/07"))
    else:
        print(f"❌ HAProxy version mismatch. Expected: 2.4.2-553dee3 2021/07/07, Got: {version_out}")
        command_statuses.append((version_cmd, False, f"HAProxy version mismatch. Expected: 2.4.2-553dee3 2021/07/07"))
    
    # Step 3a: Proxy testing for 2 ILL configuration
    print("\nStep 3a: HAProxy Proxy Testing for 2 ILL Configuration")
    proxy_tests_2ill = [
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23451' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23452' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23432' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23433' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'"
    ]
    
    working_responses_2ill = 0
    for i, cmd in enumerate(proxy_tests_2ill, 1):
        print(f"\nTesting 2 ILL Proxy {i}/4:")
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        if '"status": "Working"' in out or "200" in out or '"success":true' in out:
            print(f"✅ 2 ILL Proxy test {i} succeeded - Got 'Working' response")
            working_responses_2ill += 1
            command_statuses.append((f"2ill_proxy_test_{i}", True, f"2 ILL Proxy test {i} succeeded"))
        else:
            print(f"❌ 2 ILL Proxy test {i} failed - Expected 'Working' response")
            print(f"Response: {out[:200]}...")
            command_statuses.append((f"2ill_proxy_test_{i}", False, f"2 ILL Proxy test {i} failed"))
    
    print(f"\n2 ILL Proxy Test Summary: {working_responses_2ill}/4 tests passed")
    if working_responses_2ill == 4:
        print('✅ SUCCESS: All 4 proxy tests for 2 ILL returned {"status": "Working"}')
        print("Expected 2 ILL output achieved:")
        for i in range(4):
            print('{"status": "Working"}')
    
    # Step 3b: Proxy testing for 3 ILL configuration
    print("\nStep 3b: HAProxy Proxy Testing for 3 ILL Configuration")
    proxy_tests_3ill = [
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23451' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23452' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23453' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23432' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
        "curl --request GET --proxy 'http://127.0.0.1:23433' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'"
    ]
    
    working_responses_3ill = 0
    for i, cmd in enumerate(proxy_tests_3ill, 1):
        print(f"\nTesting 3 ILL Proxy {i}/5:")
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        
        if '"status": "Working"' in out or "200" in out or '"success":true' in out:
            print(f"✅ 3 ILL Proxy test {i} succeeded - Got 'Working' response")
            working_responses_3ill += 1
            command_statuses.append((f"3ill_proxy_test_{i}", True, f"3 ILL Proxy test {i} succeeded"))
        else:
            print(f"❌ 3 ILL Proxy test {i} failed - Expected 'Working' response")
            print(f"Response: {out[:200]}...")
            command_statuses.append((f"3ill_proxy_test_{i}", False, f"3 ILL Proxy test {i} failed"))
    
    print(f"\n3 ILL Proxy Test Summary: {working_responses_3ill}/5 tests passed")
    if working_responses_3ill == 5:
        print('✅ SUCCESS: All 5 proxy tests for 3 ILL returned {"status": "Working"}')
        print("Expected 3 ILL output achieved:")
        for i in range(5):
            print('{"status": "Working"}')
    
    # Step 4: Validate HAProxy configuration logs
    print("\nStep 4: Validating HAProxy Configuration")
    config_cmd = "cat /etc/haproxy/haproxy.cfg"
    success, config_out, config_err, config_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, config_cmd, args.ssh_port
    )
    
    print("HAProxy Configuration Summary:")
    print("=" * 80)
    # Print first 50 lines to avoid overwhelming output
    config_lines = config_out.splitlines()
    for i, line in enumerate(config_lines[:50]):
        print(f"{i+1:3d}: {line}")
    if len(config_lines) > 50:
        print(f"... (showing first 50 lines of {len(config_lines)} total lines)")
    print("=" * 80)
    
    # Validate specific HAProxy configuration elements
    config_checks = [
        ("check fall", "✅ HAProxy check fall configuration found"),
        ("server local_squid", "✅ Local squid server configuration found"),
        ("backup", "✅ Backup server configuration found"),
        ("frontend", "✅ Frontend configuration found"),
        ("backend", "✅ Backend configuration found")
    ]
    
    for search_term, success_msg in config_checks:
        if search_term.lower() in config_out.lower():
            print(success_msg)
            command_statuses.append((config_cmd, True, success_msg))
        else:
            error_msg = f"❌ {search_term} configuration not found"
            print(error_msg)
            command_statuses.append((config_cmd, False, error_msg))
    
    # Overall summary
    print(f"\n{'='*60}")
    print("HAPROXY VALIDATION SUMMARY")
    print(f"{'='*60}")
    print(f"Service Status: {'✅ Running' if 'running' in status_out.lower() or 'active' in status_out.lower() else '❌ Not Running'}")
    print(f"Version Check: {'✅ Correct (2.4.2-553dee3)' if '2.4.2-553dee3' in version_out else '❌ Incorrect'}")
    print(f"2 ILL Proxy Tests: {working_responses_2ill}/4 passed")
    print(f"3 ILL Proxy Tests: {working_responses_3ill}/5 passed")
    print(f"Configuration: {'✅ Valid' if 'check fall' in config_out.lower() else '❌ Issues detected'}")
    
    # Determine overall status
    version_ok = "2.4.2-553dee3" in version_out
    service_ok = "running" in status_out.lower() or "active" in status_out.lower()
    config_ok = "check fall" in config_out.lower()
    proxy_ok = working_responses_2ill >= 3 or working_responses_3ill >= 4  # Allow some flexibility
    
    if version_ok and service_ok and config_ok and proxy_ok:
        print("🎉 OVERALL HAPROXY STATUS: ✅ PASSED")
        command_statuses.append(("haproxy_overall", True, "HAProxy validation passed"))
    else:
        print("⚠️  OVERALL HAPROXY STATUS: ❌ FAILED")
        command_statuses.append(("haproxy_overall", False, "HAProxy validation failed"))


def task_haproxy_config_file_validation(args, command_statuses):
    print_note("HAProxy Configuration File Detailed Validation")
    
    # Read and analyze the full HAProxy configuration
    config_cmd = "cat /etc/haproxy/haproxy.cfg"
    success, config_out, config_err, config_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, config_cmd, args.ssh_port
    )
    
    if not success or not config_out.strip():
        print("❌ Failed to read HAProxy configuration file")
        command_statuses.append((config_cmd, False, "Failed to read HAProxy configuration file"))
        return
    
    print("Analyzing HAProxy Configuration File...")
    
    # Count and validate server configurations
    server_count = config_out.lower().count("server ")
    print(f"Found {server_count} server configurations")
    
    # Check for specific server types mentioned in CSV
    local_squid_servers = config_out.lower().count("server local_squid")
    backup_servers = config_out.lower().count("backup")
    
    print(f"Local squid servers: {local_squid_servers}")
    print(f"Backup servers: {backup_servers}")
    
    # Validate expected patterns from CSV example
    expected_patterns = [
        ("server local_squid_ip1", "localhost:23451", "Local squid IP1 configuration"),
        ("server local_squid_ip2", "localhost:23452", "Local squid IP2 configuration"), 
        ("server local_squid_ip3", "localhost:23453", "Local squid IP3 configuration"),
        ("check fall 2 rise 3", "", "Check fall 2 rise 3 configuration"),
        ("check fall 1 rise 6", "", "Check fall 1 rise 6 backup configuration"),
        ("inter ", "", "Inter check interval configuration"),
        ("weight ", "", "Weight configuration")
    ]
    
    print("\nValidating expected configuration patterns:")
    for pattern, context, description in expected_patterns:
        if pattern.lower() in config_out.lower():
            print(f"✅ {description}")
            command_statuses.append((config_cmd, True, description))
        else:
            print(f"❌ {description} - Pattern '{pattern}' not found")
            command_statuses.append((config_cmd, False, f"{description} - Pattern '{pattern}' not found"))
    
    # Check for frontend/backend sections
    frontend_count = config_out.lower().count("frontend")
    backend_count = config_out.lower().count("backend")
    
    print(f"\nConfiguration sections:")
    print(f"Frontend sections: {frontend_count}")
    print(f"Backend sections: {backend_count}")
    
    if frontend_count > 0 and backend_count > 0:
        print("✅ HAProxy has proper frontend and backend configuration")
        command_statuses.append((config_cmd, True, "HAProxy has proper frontend and backend configuration"))
    else:
        print("❌ HAProxy missing frontend or backend configuration")
        command_statuses.append((config_cmd, False, "HAProxy missing frontend or backend configuration"))

def task_php_timezone_validation(args, command_statuses):
    print_note("PHP Timezone Configuration Validation")
    
    # Check PHP timezone configuration
    timezone_cmd = "cat /etc/php.ini | grep -i date.timezone"
    success, timezone_out, timezone_err, timezone_rc = run_remote_cmd(
        args.ssh_host, args.ssh_user, args.ssh_key, timezone_cmd, args.ssh_port
    )
    
    print(f"Command: {timezone_cmd}")
    print(f"Output: {timezone_out}")
    
    if not timezone_out.strip():
        print("❌ No date.timezone configuration found in /etc/php.ini")
        command_statuses.append((timezone_cmd, False, "No date.timezone configuration found in /etc/php.ini"))
        return
    
    # Check if timezone is set to Asia/Calcutta
    timezone_found = False
    
    for line in timezone_out.splitlines():
        line = line.strip()
        if 'date.timezone' in line.lower() and 'asia/calcutta' in line.lower():
            timezone_found = True
            print(f"✅ PHP timezone is correctly configured: {line}")
            command_statuses.append((timezone_cmd, True, f"PHP timezone is correctly configured: {line}"))
            break
    
    if not timezone_found:
        print("❌ PHP timezone is not set to Asia/Calcutta")
        print("Expected: date.timezone = \"Asia/Calcutta\"")
        command_statuses.append((timezone_cmd, False, "PHP timezone is not set to Asia/Calcutta"))

def print_manual_verification_checklist(args):
    print("\n" + "="*80)
    print("MANUAL VERIFICATION CHECKLIST")
    print("="*80)
    print("The following items need to be verified/completed manually:\n")
    
    # Extract server number for even/odd determination
    server_name = args.ssh_host
    try:
        # Extract number from hostname (e.g., 080-33 -> 33)
        server_number = int(server_name.split('-')[1].split('.')[0])
        is_even = server_number % 2 == 0
        cron_type = "EVEN" if is_even else "ODD"
        cron_url = "https://build.corp.exotel.in:8080/job/ts_%20log_uploader_cron_even/" if is_even else "https://build.corp.exotel.in:8080/job/ts_logs_uploader_cron_odd/"
    except:
        cron_type = "UNKNOWN (check server number)"
        cron_url = "https://build.corp.exotel.in:8080/job/ts_%20log_uploader_cron_even/ OR https://build.corp.exotel.in:8080/job/ts_logs_uploader_cron_odd/"
    
    print(f"1. 📝 ADD HOSTNAME TO CRON JOBS")
    print(f"   Server: {server_name} ({cron_type} server)")
    print(f"   Action: Add hostname '{server_name}' to the appropriate cron job:")
    print(f"   URL: {cron_url}")
    print(f"   Note: Add EVEN number servers to 'ts_%20log_uploader_cron_even'")
    print(f"         Add ODD number servers to 'ts_logs_uploader_cron_odd'")
    print(f"   This cron job uploads logs using the script deployed in step 3.\n")
    
    print(f"2. 🌐 ILLs WHITELISTED IN CLOUD SECURITY GROUPS")
    print(f"   Action: Ensure all ILL IPs for server '{server_name}' are whitelisted")
    print(f"   Check: Cloud security groups configuration")
    print(f"   Verify: All outbound ILL traffic is allowed\n")
    
    print(f"3. 🔧 UPDATE IAX.CONF MASTER/SLAVE CONFIGURATION")
    print(f"   Action: Update master/slave configuration in IAX.conf")
    print(f"   File: /etc/asterisk/iax.conf")
    print(f"   Check: Proper master/slave relationship configured")
    print(f"   Verify: IAX trunk configuration is correct\n")
    
    print(f"4. 🧪 COMPREHENSIVE CALL TESTING")
    print(f"   Perform the following tests on server '{server_name}':")
    print(f"   ✓ Test Call - Make inbound and outbound test calls")
    print(f"   ✓ CDR Entry - Verify call detail records are created")
    print(f"   ✓ Uidstampmap Entry - Check UID stamp mapping entries")
    print(f"   ✓ AMI Entry - Verify Asterisk Manager Interface events")
    print(f"   ✓ Recording Upload - Check recordings are uploaded to S3")
    print(f"   ✓ Recording Local File Deletion - Verify local files are cleaned up")
    print(f"   ✓ Make OB Call - Test outbound calling functionality")
    print(f"   ✓ Billing - Verify billing records are generated")
    print(f"   ✓ Inbox - Check inbox/voicemail functionality\n")
    
    print("="*80)
    print("IMPORTANT: Complete ALL manual verification steps before")
    print("marking the server deployment as SUCCESSFUL!")
    print("="*80)

def main():
    parser = argparse.ArgumentParser(description="Merged Server Validation & Service Check Script")
    # parser.add_argument('--expected-hostname', required=True, help='Expected hostname for verification')
    # parser.add_argument('--twilix-server-code', required=False, help='Server code for Twilix SQL')
    parser.add_argument('--ssh-host', required=True, help='Remote SSH host')
    parser.add_argument('--ssh-user', required=True, help='Remote SSH username')
    parser.add_argument('--ssh-key', required=True, help='Path to SSH private key')
    parser.add_argument('--ssh-port', type=int, default=22, help='SSH port (default: 22)')
    args = parser.parse_args()

    command_statuses = []

    # Call your new modular tasks her

    task_user_verification(args, command_statuses)
    task_ssh_configs(args, command_statuses)
    task_bash_configs(args, command_statuses)
    task_aws_credentials(args, command_statuses)
    # Task 1: Hostname verification
    print_note("Hostname is used by AHN/Amix/Eventshipper while creating AMI events and shipping them to asteriskStoreDB. This has to be correct on the server end, so that we only ship events with the appropriate server name")
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, 'hostname', args.ssh_port)
    if out.strip() == args.ssh_host:
        print("✅ Hostname matches expected: {}".format(args.ssh_host))
        command_statuses.append(('hostname', True, "Hostname matches expected: {}".format(args.ssh_host)))
    else:
        print("❌ Hostname mismatch! Expected: {}, Got: {}".format(args.ssh_host, out.strip()))
        command_statuses.append(('hostname', False, "Hostname mismatch! Expected: {}, Got: {}".format(args.ssh_host, out.strip())))

    # Task 2: Timezone verification
    print_note("Timezone should be IST")
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, 'date', args.ssh_port)
    if "IST" in out:
        print("✅ Timezone is IST")
        command_statuses.append(('date', True, "Timezone is IST"))
    else:
        print("❌ Timezone is not IST! Output:", out)
        command_statuses.append(('date', False, "Timezone is not IST! Output: {}".format(out)))

    # Task 3: sillyio.yml ob_channel_threshold
    cmd = "less /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml | grep ob_channel_threshold"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ sillyio.yml ob_channel_threshold checked successfully")
        print(out)
        command_statuses.append((cmd, True, "Checked sillyio.yml ob_channel_threshold"))
    else:
        print("❌ Failed to check sillyio.yml ob_channel_threshold")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"sillyio.yml ob_channel_threshold check failed: {err}"))
        if err:
            print("STDERR:", err)

    # Task 4: Twilix SQL
    print_note("""Make sure the span and the pilot numbers match.
In twilix small table, we store the span and pilot connected to the span. When an incoming call lands on a server, the appropriate span mappings on the server in sillyio.yml are 
used to determine the operator and other information. If this span mapping is wrong bad things can happen. [add more info here]""")
    if args.ssh_host:
        try:
            run_twilix_db_queries(args.ssh_host)
            print("✅ Twilix SQL queries completed successfully")
            command_statuses.append(("Twilix SQL", True, "Twilix SQL completed"))
        except Exception as e:
            print(f"❌ Twilix SQL queries failed: {e}")
            command_statuses.append(("Twilix SQL", False, f"Twilix SQL failed: {e}"))
    else:
        print("❌ No SSH host provided, skipping Twilix SQL")
        command_statuses.append(("Twilix SQL", False, "No SSH host provided, skipping SQL"))


    # Task 5: Recording directory permissions
    for d in ["/var/log/exotel/recordings/sgp1/", "/var/log/exotel/recordings/mum1/", "/var/log/exotel/recordings/causix_recordings/"]:
        cmd = "sudo ls -ld {}".format(d)
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if "drwxrwxr-x" in out or " 776 " in out or out.endswith(" 776"):
            print("✅ {} has correct permissions (776)".format(d))
            command_statuses.append((cmd, True, "{} has correct permissions (776)".format(d)))
        else:
            print("❌ {} permissions not 776! Output: {}".format(d, out))
            command_statuses.append((cmd, False, "{} permissions not 776! Output: {}".format(d, out)))

    # Task 6: Connectivity to twilix-internal
    print_note("Twilix and internal.twilix to pick up details like the voice-flow that the particular call has to connect to from both the stamps.")
    urls = [
        "https://twilix.exotel.com/v1/accounts",
        "https://internal.twilix.exotel.com/v1/accounts",
        "https://twilix.mum1.exotel.com/v1/accounts",
        "https://internal.twilix.mum1.exotel.com/v1/accounts"
    ]
    for url in urls:
        cmd = "curl -k '{}'".format(url)
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if out:
            print("✅ Got response from {}".format(url))
            command_statuses.append((cmd, True, "Got response from {}".format(url)))
        else:
            print("❌ No response from {}".format(url))
            command_statuses.append((cmd, False, "No response from {}".format(url)))

    # Task 7: Connectivity with obelix appengine
    print_note("make sure you got some response from both the stamps and not error. Appengine deals with executing the voice-flow, maintaining the number free/busy as well as updating the status of the call at the end of the call,")
    for url in [
        "https://appengine.exotel.com/auth/login",
        "https://appengine.mum1.exotel.com/auth/login"
    ]:
        cmd = "curl '{}'".format(url)
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if out:
            print("✅ Got response from {}".format(url))
            command_statuses.append((cmd, True, "Got response from {}".format(url)))
        else:
            print("❌ No response from {}".format(url))
            command_statuses.append((cmd, False, "No response from {}".format(url)))

    # Task 8: Service status checks (merged from sanity_check_script.py)
    print_note("Checking important systemd services")
    service_commands = [
        "sudo systemctl status sshd",
        # "sudo grep -E 'asterisk|exomon|recotrix' /etc/passwd",
        # "sudo grep \"exotel@prod-build-node\" /home/asterisk/.ssh/authorized_keys",
        # "sudo grep \"exotel@Cron-Machine2\" /home/asterisk/.ssh/authorized_keys",
        # "sudo ls -l /home/asterisk/.ssh",
        # "sudo ls -l /home/exomon/.ssh",
        # "sudo ls -a /home/asterisk/",
        # "sudo cat /home/asterisk/.aws/credentials",
        # "sudo cat /root/.aws/credential",
        "sudo systemctl status fail2ban",
        "sudo grep -i \"22000\" /etc/ssh/sshd_config",
        "sudo systemctl status beanstalkd",
        "sudo systemctl status dnsmasq",
        "sudo systemctl status rsyslog",
        "sudo systemctl status squid",
        "sudo systemctl status vsftpd",
        "sudo systemctl status asterisk",
        "sudo systemctl status legolas-ts",
        "sudo systemctl status amix",
        "sudo systemctl status causix",
        "sudo systemctl status causixenqueuer",
        "sudo systemctl status ahn",
        "sudo systemctl status eventshipper",
        "sudo systemctl status voipmonitor",
        "sudo systemctl status fangorn",
        "sudo systemctl status firefoot-ts",
        "sudo systemctl status haproxy",
        "sudo systemctl status mysqld",
        "sudo service irqbalance status",
        "sudo service crond status",
        "sudo /opt/jruby-1.7.1/bin/jruby -S gem list", 
        "sudo bash /home/asterisk/traffic-shaper/trafficShaper.sh status"
    ]
    for i, cmd in enumerate(service_commands, 1):
        print("\n\n --------------- Executing command {} :- {} --------------------------------- \n".format(i, cmd))
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        print(out)
        if err:
            print("STDERR:", err)
        if not success:
            print("Command {} failed".format(i))
            command_statuses.append((cmd, False, "Command {} failed".format(i)))
        else:
            command_statuses.append((cmd, True, "Command {} successful".format(i)))

    # Task 9: NTPD status (already checked above, but included for completeness)
    cmd = "sudo systemctl status ntpd"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ NTPD status checked successfully")
        print(out)
        command_statuses.append((cmd, True, "NTPD status checked"))
    else:
        print("❌ NTPD status check failed")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"NTPD status check failed: {err}"))
        if err:
            print("STDERR:", err)

    cmd = "ntpstat"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ ntpstat checked successfully")
        print(out)
        command_statuses.append((cmd, True, "ntpstat checked"))
    else:
        print("❌ ntpstat check failed")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"ntpstat check failed: {err}"))
        if err:
            print("STDERR:", err)

    # Task 10: Check HAProxy & Squid logs
    print_note("these logs should not be empty")
    for log in ["/var/log/squid/access.log", "/var/log/squid/cache.log", "/var/log/haproxy/admin.log"]:
        cmd = "sudo tail -n 10 {}".format(log)
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if out:
            print("✅ {} is not empty".format(log))
            command_statuses.append((cmd, True, "{} is not empty".format(log)))
        else:
            print("❌ {} is empty or not found".format(log))
            command_statuses.append((cmd, False, "{} is empty or not found".format(log)))

    # Task 11: rsyslog config files
    print_note("""The following rsyslog configs should be present:
    - haproxy.conf  
    - impstats.conf  
    - logs.conf  
    - metrics.conf""")
    cmd = "ls -l /etc/rsyslog.d/"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    for conf in ["haproxy.conf", "impstats.conf", "logs.conf", "metrics.conf"]:
        if conf in out:
            print("✅ {} present".format(conf))
            command_statuses.append((cmd, True, "{} present".format(conf)))
        else:
            print("❌ {} missing".format(conf))
            command_statuses.append((cmd, False, "{} missing".format(conf)))

    # Task 12: IP whitelisting connectivity
    for host, port in [("rsyslog.mum1.exotel.in", 9800), ("kafka-1.internal.exotel.in", 9092), ("kafka-2.internal.exotel.in", 9092)]:
        cmd = "nc -zvw2 {} {}".format(host, port)
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if "Connected" in out or "Connected" in err or "Escape character" in out or "Escape character" in err:
            print("✅ Telnet to {}:{} successful".format(host, port))
            command_statuses.append((cmd, True, "Telnet to {}:{} successful".format(host, port)))
        else:
            print("❌ Telnet to {}:{} failed".format(host, port))
            command_statuses.append((cmd, False, "Telnet to {}:{} failed".format(host, port)))

    # Task 13: Adhearsion credentials
    cmd = "grep 'default_sid' /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        if 'default_sid' in out:
            print("✅ Credentials start with default_sid")
            command_statuses.append((cmd, True, "Credentials start with default_sid"))
        else:
            print("❌ Credentials do not start with default_sid or not found")
            command_statuses.append((cmd, False, "Credentials do not start with default_sid or not found"))
    else:
        print("❌ Failed to check Adhearsion credentials")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"Failed to check Adhearsion credentials: {err}"))
        
    print_note("""if you found no creds and wrong credentials, Please generate it and source it in DB exotel_code/twilix/scripts/generateTSCreds.php
E.G: php generateTSCreds.php 0229

Commit it to code-base with new branch and make pull request to voice dri""")

    # Task 14: Hyperthreading check
    cmd = "lscpu | grep -i -E '^CPU\\(s\\):|core|socket'"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ Hyperthreading check (lscpu) completed successfully")
        print(out)
        command_statuses.append((cmd, True, "Checked Hyperthreading (lscpu)"))
    else:
        print("❌ Hyperthreading check (lscpu) failed")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"Hyperthreading check (lscpu) failed: {err}"))
        if err:
            print("STDERR:", err)

    cmd = "grep -E 'cpu cores|siblings|physical id' /proc/cpuinfo | xargs -n 11 echo |sort |uniq"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ Hyperthreading check (cpuinfo) completed successfully")
        print(out)
        command_statuses.append((cmd, True, "Checked Hyperthreading (cpuinfo)"))
    else:
        print("❌ Hyperthreading check (cpuinfo) failed")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"Hyperthreading check (cpuinfo) failed: {err}"))
        if err:
            print("STDERR:", err)

    cmd = "sudo dmidecode | grep Count"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ Hyperthreading check (dmidecode) completed successfully")
        print(out)
        command_statuses.append((cmd, True, "Checked Hyperthreading (dmidecode)"))
    else:
        print("❌ Hyperthreading check (dmidecode) failed")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"Hyperthreading check (dmidecode) failed: {err}"))
        if err:
            print("STDERR:", err)

    # Task 15: sillyio config verification
    cmd = "grep s3_recording_bucket /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ sillyio s3_recording_bucket config checked successfully")
        print(out)
        command_statuses.append((cmd, True, "Checked sillyio s3_recording_bucket config"))
    else:
        print("❌ Failed to check sillyio s3_recording_bucket config")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"sillyio s3_recording_bucket config check failed: {err}"))
        if err:
            print("STDERR:", err)

    cmd = "grep conference_master /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    
    if success:
        print("✅ sillyio conference_master config checked successfully")
        print(out)
        command_statuses.append((cmd, True, "Checked sillyio conference_master config"))
    else:
        print("❌ Failed to check sillyio conference_master config")
        print(f"Error: {err}")
        command_statuses.append((cmd, False, f"sillyio conference_master config check failed: {err}"))
        if err:
            print("STDERR:", err)

    # Task 16: SSH key verification
    for key in ["exotel@prod-build-node", "exotel@Cron-Machine2"]:
        cmd = "grep '{}' /home/asterisk/.ssh/authorized_keys".format(key)
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if out:
            print("✅ SSH key for {} found".format(key))
            command_statuses.append((cmd, True, "SSH key for {} found".format(key)))
        else:
            print("❌ SSH key for {} not found".format(key))
            command_statuses.append((cmd, False, "SSH key for {} not found".format(key)))

    task_check_rsyslog_mum1(args, command_statuses)
    task_check_ahn_timezone(args, command_statuses)
    task_check_nproc_value(args, command_statuses)
    task_check_manager_interface_actionid(args, command_statuses)
    task1_check_local_http_ports(args, command_statuses)
    task_verify_route_switcher_config(args, command_statuses)
    task_sillyio_config_verification(args, command_statuses)
    task_squid_config_validation(args, command_statuses)
    task_squid_comprehensive_validation(args, command_statuses)
    task_squid_detailed_status_validation(args, command_statuses)
    task_squid_proxy_working_validation(args, command_statuses)
    task2_check_ip_platform(args, command_statuses)
    task3_check_active_channel_script(args, command_statuses)
    task_verify_sbc_domains_in_hosts(args, command_statuses)
    task5_tcp_connection_recovery(args, command_statuses)
    task6_beanstalkd_file_limit(args, command_statuses)
    task7_check_iptables(args, command_statuses)
    task8_logrotate_configs(args, command_statuses)
    task9_squid_health_and_proxy_checks(args, command_statuses)
    task10_squid_status(args, command_statuses)
    task11_haproxy_status(args, command_statuses)
    task12_check_recording_status(args, command_statuses)
    task13_check_for_AMI_Events_status(args, command_statuses)
    task14_check_asterisk_srtp(args, command_statuses)
    task_haproxy_detailed_status_validation(args, command_statuses)
    task_haproxy_config_file_validation(args, command_statuses)
    task_php_timezone_validation(args, command_statuses)
    
    

    # Summary of failed commands
    print("\n\n --------------- Command Summary: --------------------------------- \n")
    for cmd, status, msg in command_statuses:
        mark = "✅" if status else "❌"
        print(f"{mark} {cmd}\n    {msg}")
    
    # Add the manual verification checklist
    print_manual_verification_checklist(args)

if __name__ == "__main__":
    main()