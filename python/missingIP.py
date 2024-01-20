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

    # Use the first IP from the file and append '.0/24' to create the subnet
    first_ip = input_ips[0].split('.')[0:3]
    first_ip.append('0/24')
    subnet = ".".join(first_ip)

    missing_ips = get_missing_ips(input_ips, subnet)

    # Save the results to a file, overwriting existing content
    with open("results.txt", "w") as result_file:
        for ip in missing_ips:
            result_file.write(ip + "\n")

    print("\nMissing IPs written to results.txt")

if __name__ == "__main__":
    main()
