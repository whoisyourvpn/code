import time
import csv
import asyncio
import aiohttp
import logging
import subprocess
import requests
from bs4 import BeautifulSoup

def VPN(action, myvpn=None):
    openvpn_gui_path = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"
    valid_actions = ["connect", "disconnect", "reconnect", "status"]
    if action in valid_actions:
        if myvpn:
            command = f'"{openvpn_gui_path}" --command {action} "{myvpn}"'
        else:
            command = f'"{openvpn_gui_path}" --command {action}'
        subprocess.Popen(command, shell=True)
    else:
        print("Invalid action:", action)

def PublicIPAddress():
    try:
        response = requests.get("http://whatismyip.akamai.com/")
        return response.text.strip()
    except:
        return "Unable to fetch public IP"

def WaitUntilVPNConnected():
    print("Waiting for VPN to connect...")
    time.sleep(20)
    public_ip = PublicIPAddress()
    if public_ip != "Unable to fetch public IP":
        print(f"Connected with public IP: {public_ip}")
    else:
        print("VPN not connected")

async def process_ip(session, writer, ip, url):
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 429:
                print(f"{ip}, Rate limit exceeded")
                logging.error(f"{ip}, Rate limit exceeded")
                await asyncio.sleep(10)
                return
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            h1_tag = soup.find("h1", class_="ddc mb-3 text-left")
            if h1_tag:
                data = h1_tag.get_text(strip=True)
                data = data.replace(ip + ' - ', '').strip()
                if data.lower() == 'not anonymous':
                    data = 'Anonymous'
                writer.writerow([ip, data])
                print(f"{ip},{data}")
            else:
                logging.debug(f"No h1_tag found for IP: {ip}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

async def fetch_all_ips(writer, start_ip, end_ip, subnet):
    async with aiohttp.ClientSession() as session:
        tasks = [process_ip(session, writer, subnet + str(i), f"https://example.com/{subnet}{i}") for i in range(start_ip, min(end_ip, 256))]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    subnet = input("Enter subnet to scan (example: 198.7.61.): ")
    start_ip = int(input("Enter the first IP to scan (0-255): "))
    filename = subnet.replace('.', '-') + '.csv'
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ip', 'name'])
        continue_processing = True

        while continue_processing and start_ip < 256:
            myvpn = r"us.protonvpn.net.udp.ovpn"
            VPN("connect", myvpn)
            WaitUntilVPNConnected()
            end_ip = start_ip + 15
            asyncio.run(fetch_all_ips(writer, start_ip, end_ip, subnet))
            print(f"Data saved to {filename}")
            logging.info(f"Data saved to {filename}")
            VPN("disconnect", myvpn)
            start_ip = end_ip

            if end_ip < 256:
                user_input = input("Processing completed for this batch of 15 IPs. Hit any key to continue or type 'exit' to stop processing: ")
                if user_input.lower() == 'exit':
                    continue_processing = False
