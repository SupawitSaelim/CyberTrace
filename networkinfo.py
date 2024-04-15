import socket
import netifaces

def get_private_ip_hostname_prefix_and_mac():
    hostname = socket.gethostname()
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface != "lo":
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ipv4_info = addresses[netifaces.AF_INET][0]
                ip_address = ipv4_info.get("addr")
                netmask = ipv4_info.get("netmask")
                if not ip_address.startswith("127."):
                    prefix = sum(bin(int(x)).count('1') for x in netmask.split('.'))
                    mac_address = addresses[netifaces.AF_LINK][0]["addr"]
                    return hostname, ip_address, prefix, mac_address
    return None, None, None, None

if __name__ == "__main__":
    computer_name, private_ip, prefix, mac_address = get_private_ip_hostname_prefix_and_mac()

    if computer_name and private_ip and prefix and mac_address:
        print("Your Computer Name is:", computer_name)
        print("Your Computer Private IP Address is:", private_ip)
        print("Network Prefix Length (Subnet Mask):", prefix)
        print("MAC Address:", mac_address)
    else:
        print("Unable to retrieve computer name, private IP address, network prefix length, and MAC address.")
