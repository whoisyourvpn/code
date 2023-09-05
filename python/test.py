import subprocess
import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
import logging
import time

def protonvpn_login(username, password):
    command = f"echo '{password}' | sudo -S protonvpn login {username}"
    proc = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if b"Successfully logged in" in proc.stdout:
        return True
    return False

def protonvpn_connect():
    command = "echo 'your_sudo_password_here' | sudo -S protonvpn c -r"
    subprocess.run(command, shell=True)

def PublicIPAddress():
    response = requests.get("http://whatismyip.akamai.com/")
    return response.text.strip()

def WaitUntilVPNConnected():
    time.sleep(20)
    public_ip = PublicIPAddress()
    print(f"Connected with public IP: {public_ip}")

async def process_ip(session, writer, ip, url):
    async with session.get(url, timeout=30) as response:
        if response.status == 429:
            print(f"{ip}, Rate limit exceeded")
            protonvpn_connect()
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

async def fetch_all_ips(writer, start_ip, end_ip, subnet):
    async with aiohttp.ClientSession() as session:
        tasks = [process_ip(session, writer, f"{subnet}{i}", f"https://spur.us/context/{subnet}{i}") for i in range(start_ip, min(end_ip, 256))]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    username = input("Enter your ProtonVPN username: ")
    password = input("Enter your ProtonVPN password: ")

    if not protonvpn_login(username, password):
        print("Failed to log in to ProtonVPN.")
        exit(1)

    print("Successfully logged in to ProtonVPN.")

    subnet = input("Enter subnet to scan (example: 198.7.61.): ")
    start_ip = int(input("Enter the first IP to scan (0-255): "))
    filename = subnet.replace('.', '-') + '.csv'
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ip', 'name'])
        while start_ip < 256:
            protonvpn_connect()
            WaitUntilVPNConnected()
            end_ip = start_ip + 15
            asyncio.run(fetch_all_ips(writer, start_ip, end_ip, subnet))
            print(f"Data saved to {filename}")
            start_ip = end_ip
