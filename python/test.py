import time
import csv
import asyncio
import aiohttp
import logging
import subprocess
import requests
from bs4 import BeautifulSoup

def protonvpn_login(username, password):
    command = f"sudo protonvpn login {username}"
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.write(password.encode('utf-8'))
    proc.stdin.write(b'\n')
    proc.stdin.flush()
    stdout, stderr = proc.communicate()
    if b"Successfully logged in" in stdout:
        return True
    return False

# Prompt for ProtonVPN credentials
username = input("Enter your ProtonVPN username: ")
password = input("Enter your ProtonVPN password: ")

# Log in to ProtonVPN
if protonvpn_login(username, password):
    print("Successfully logged in to ProtonVPN.")
else:
    print("Failed to log in to ProtonVPN.")
    exit(1)

def VPN(action):
    if action == 'connect':
        command = "sudo protonvpn c -r"
        subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif action == 'disconnect':
        command = "sudo protonvpn d"
        subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def PublicIPAddress():
    response = requests.get("http://whatismyip.akamai.com/")
    return response.text.strip()

def WaitUntilVPNConnected():
    time.sleep(20)
    public_ip = PublicIPAddress()
    print(f"Connected with public IP: {public_ip}")

async def process_ip(session, writer, ip, url):
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 429:
                print(f"{ip}, Rate limit exceeded")
                VPN("disconnect")
                time.sleep(10)
                VPN("connect")
                WaitUntilVPNConnected()
                return
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            h1_tag = soup.find("h1", class_="ddc mb-3 text-left")
            if h1_tag:
                data = h1_tag.get_text(strip=True).replace(ip + ' - ', '').strip()
                if data.lower() == 'not anonymous':
                    data = 'Anonymous'
                writer.writerow([ip, data])
                print(f"{ip},{data}")
    except asyncio.TimeoutError:
        print(f"{ip}, Timeout occurred")
        VPN("disconnect")
        time.sleep(10)
        VPN("connect")
        WaitUntilVPNConnected()
        return
    except Exception as e:
        print(f"An error occurred: {e}")

async def fetch_all_ips(writer, start_ip, end_ip, subnet):
    async with aiohttp.ClientSession() as session:
        tasks = [process_ip(session, writer, f"{subnet}{i}", f"https://example.com/{subnet}{i}") for i in range(start_ip, min(end_ip, 256))]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    subnet = input("Enter subnet to scan (example: 198.7.61.): ")
    start_ip = int(input("Enter the first IP to scan (0-255): "))
    filename = subnet.replace('.', '-') + '.csv'
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ip', 'name'])
        while start_ip < 256:
            VPN("connect")
            WaitUntilVPNConnected()
            end_ip = start_ip + 15
            asyncio.run(fetch_all_ips(writer, start_ip, end_ip, subnet))
            print(f"Data saved to {filename}")
            VPN("disconnect")
            time.sleep(20)
            start_ip = end_ip
