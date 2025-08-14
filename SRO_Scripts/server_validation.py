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
        cmd = f"ls -la /home/{user}/.ssh"
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        if "No such file or directory" in out or "No such file or directory" in err:
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
        if out.strip():
            print(f"✅ {key} found in authorized_keys")
            command_statuses.append((cmd, True, f"{key} found in authorized_keys"))
        else:
            print(f"❌ {key} NOT found in authorized_keys")
            command_statuses.append((cmd, False, f"{key} NOT found in authorized_keys"))

def task_bash_configs(args, command_statuses):
    print_note("Bash Configs: Check for bash config/history files in /home/asterisk/")
    cmd = "ls -la /home/asterisk/"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
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
    print(out)
    # Add logic to check for required rules
    command_statuses.append((cmd, True, "Checked iptables rules"))

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
        "squid -v"
    ]
    for cmd in cmds:
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        print(out)
    # Add logic to check version and status
    command_statuses.append((cmds[0], True, "Checked Squid status"))
    command_statuses.append((cmds[1], True, "Checked Squid version"))

def task11_haproxy_status(args, command_statuses):
    print_note("Task 11: HAProxy status")
    cmds = [
        "sudo service haproxy status",
        "haproxy -v"
    ]
    for cmd in cmds:
        success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
        print(out)
    # Add logic to check version and status
    command_statuses.append((cmds[0], True, "Checked HAProxy status"))
    command_statuses.append((cmds[1], True, "Checked HAProxy version"))

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
    if not success:
        command_statuses.append((cmd, False, "sillyio.yml ob_channel_threshold not found"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "Checked sillyio.yml ob_channel_threshold"))

    # Task 4: Twilix SQL
    print_note("""Make sure the span and the pilot numbers match.
In twilix small table, we store the span and pilot connected to the span. When an incoming call lands on a server, the appropriate span mappings on the server in sillyio.yml are 
used to determine the operator and other information. If this span mapping is wrong bad things can happen. [add more info here]""")
    if args.ssh_host:
        run_twilix_db_queries(args.ssh_host)
    else:
        print("No --twilix-server-code provided, skipping SQL.")
    command_statuses.append(("Twilix SQL", True, "Twilix SQL completed"))


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
    if not success:
        command_statuses.append((cmd, False, "NTPD status check failed"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "NTPD status checked"))

    cmd = "ntpstat"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if not success:
        command_statuses.append((cmd, False, "NTPD status check failed"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "NTPD status checked"))

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
    if 'default_sid' in out:
        print("✅ Credentials start with default_sid")
        command_statuses.append((cmd, True, "Credentials start with default_sid"))
    else:
        print("❌ Credentials do not start with defaultts022 or not found")
        command_statuses.append((cmd, False, "Credentials do not start with defaultts022 or not found"))
    print_note("""if you found no creds and wrong credentials, Please generate it and source it in DB exotel_code/twilix/scripts/generateTSCreds.php
E.G: php generateTSCreds.php 0229

Commit it to code-base with new branch and make pull request to voice dri""")
    command_statuses.append((cmd, True, "Checked Adhearsion credentials"))

    # Task 14: Hyperthreading check
    cmd = "lscpu | grep -i -E '^CPU\\(s\\):|core|socket'"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if not success:
        command_statuses.append((cmd, False, "Hyperthreading check failed"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "Checked Hyperthreading"))

    cmd = "grep -E 'cpu cores|siblings|physical id' /proc/cpuinfo | xargs -n 11 echo |sort |uniq"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if not success:
        command_statuses.append((cmd, False, "Hyperthreading check failed"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "Checked Hyperthreading"))

    cmd = "sudo dmidecode | grep Count"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if not success:
        command_statuses.append((cmd, False, "Hyperthreading check failed"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "Checked Hyperthreading"))

    # Task 15: sillyio config verification
    cmd = "grep s3_recording_bucket /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if not success:
        command_statuses.append((cmd, False, "sillyio config verification failed"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "Checked sillyio config"))

    cmd = "grep conference_master /home/asterisk/adhearsion/adhearsion/sillyio/components/sillyio/sillyio.yml"
    success, out, err, rc = run_remote_cmd(args.ssh_host, args.ssh_user, args.ssh_key, cmd, args.ssh_port)
    if not success:
        command_statuses.append((cmd, False, "sillyio config verification failed"))
    print(out)
    if err:
        print("STDERR:", err)
    command_statuses.append((cmd, True, "Checked sillyio config"))

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
    
    

    # Summary of failed commands
    print("\n\n --------------- Command Summary: --------------------------------- \n")
    for cmd, status, msg in command_statuses:
        mark = "✅" if status else "❌"
        print(f"{mark} {cmd}\n    {msg}")

if __name__ == "__main__":
    main()