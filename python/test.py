import subprocess
import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
import logging
import time
import pexpect

def protonvpn_login(username, password):
    child = pexpect.spawn(f'protonvpn-cli login {username}')
    child.expect('Password:')
    child.sendline(password)
    index = child.expect(['Successfully logged in.', 'Invalid username or password'], timeout=30)
    if index == 0:
        return True
    else:
        return False

def protonvpn_connect():
    command = "sudo protonvpn-cli c -r"
    subprocess.run(command, shell=True)

def protonvpn_disconnect():
    command = "sudo protonvpn-cli d"
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
            protonvpn_disconnect()
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
            protonvpn_disconnect()
            time.sleep(20)
            start_ip = end_ip
