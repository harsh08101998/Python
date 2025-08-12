import os
import sys
import re

#sudo python3 vlan_config.py ens256 10:192.168.10.123 23:192.168.23.50


def is_root():
    return os.geteuid() == 0

def usage():
    print(f"Usage: {sys.argv[0]} <parent-interface> <vlan-id>:<ip-address> [<vlan-id>:<ip-address> ...]")
    print(f"Example: {sys.argv[0]} ens256 10:192.168.10.123 23:192.168.23.50")
    sys.exit(1)

def main():
    src_file=sys.argv[1]
    # if not is_root():
    #     print("Please run as root.")
    #     sys.exit(1)

    # if len(sys.argv) < 3:
    #     usage()

    parent_if = sys.argv[1]
    entries = sys.argv[2:]

    for entry in entries:
        if ':' not in entry:
            print(f"Invalid input: {entry}. Must be in format vlan-id:ip-address")
            continue

        vlan_id, ipaddr = entry.split(':', 1)

        if not vlan_id.isdigit() or not re.match(r'^\d+\.\d+\.\d+\.\d+$', ipaddr):
            print(f"Invalid input: {entry}. Must be in format vlan-id:ip-address")
            continue

        # Derive gateway
        octets = ipaddr.split('.')
        gateway = f"{octets[0]}.{octets[1]}.{octets[2]}.1"

        vlan_if = f"{parent_if}.{vlan_id}"
        cfg_file = f"{vlan_if}"
        # cfg_file = f"/etc/sysconfig/network-scripts/ifcfg-{vlan_if}"

        print(f"Creating VLAN interface {vlan_if} with IP {ipaddr} and Gateway {gateway}")

        config = f"""DEVICE={vlan_if}
NAME={vlan_if}
IPADDR={ipaddr}
GATEWAY={gateway}
"""
        params = ('NAME=', 'IPADDR=', 'GATEWAY=', 'DEVICE=')
        with open(src_file, 'r') as f:
            lines = f.readlines()
        filtered_lines = [line for line in lines if not line.startswith(params)]

        try:
            with open(cfg_file, 'w') as f:
                f.write(config)
                f.writelines(filtered_lines)
        except Exception as e:
            print(f"Failed to write {cfg_file}: {e}")

    print("configs added")

if __name__ == "__main__":
    main()