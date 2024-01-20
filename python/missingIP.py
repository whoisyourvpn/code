import ipaddress

def get_missing_ips(ip_list, subnet):
    # Convert the list of IPs to a set for faster lookup
    ip_set = set(ip_list)

    # Create a set of all IPs in the subnet
    all_ips = set(str(ip) for ip in ipaddress.IPv4Network(subnet, strict=False))

    # Find missing IPs by subtracting the set of given IPs from the set of all IPs
    missing_ips = all_ips - ip_set

    return sorted(list(missing_ips))

def main():
    # Read IPs from file
    with open("ips.txt", "r") as file:
        input_ips = [line.strip() for line in file if line.strip()]

    subnet = input("Enter the subnet in CIDR notation (e.g., 1.1.1.0/24): ")

    missing_ips = get_missing_ips(input_ips, subnet)

    print("\nMissing IPs:")
    for ip in missing_ips:
        print(ip)

if __name__ == "__main__":
    main()
