import requests
import time
from tqdm import tqdm

def get_ip():
    response = requests.get('http://whatismyip.akamai.com/')
    return response.text.strip()

def load_ips():
    try:
        with open('ips.txt', 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def main():
    seen_ips = load_ips()
    with open('ips.txt', 'a') as f:
        f.write('Start\n')  # Annotating start of the script
        f.flush()
        try:
            for _ in tqdm(iter(int, 1)):  # infinite loop with visual output
                try:
                    ip = get_ip()
                    if ip not in seen_ips:
                        print(f'New IP found: {ip}')
                        seen_ips.add(ip)
                        f.write(ip + '\n')
                        f.flush()
                    else:
                        print('Skipping...')  # Output "skipping..." if IP is duplicated
                except requests.exceptions.RequestException as e:
                    print(f'An error occurred: {e}')
                time.sleep(5)  # pause for 5 seconds between requests
        except KeyboardInterrupt:
            f.write('Stop\n')  # Annotating stop of the script
            f.flush()

if __name__ == "__main__":
    main()
