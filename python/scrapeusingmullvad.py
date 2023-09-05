import subprocess
import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
import logging
import time

def mullvad_connect():
    subprocess.run("mullvad connect", shell=True)

def mullvad_disconnect():
    subprocess.run("mullvad disconnect", shell=True)

def mullvad_status():
    result = subprocess.run("mullvad status", stdout=subprocess.PIPE, shell=True)
    status = result.stdout.decode().strip()
    return 'Connected' in status

def wait_until_vpn_connected():
    while True:
        if mullvad_status():
            print("Connected to Mullvad VPN.")
            break
        print("Waiting for connection status to change...")
        time.sleep(5)

async def process_ip(session, writer, ip, url, retries=3):
    for _ in range(retries):
        try:
            async with session.get(url, timeout=60) as response:
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                h1_tag = soup.find("h1", class_="ddc mb-3 text-left")
                if h1_tag:
                    data = h1_tag.get_text(strip=True).replace(ip + ' - ', '').strip()
                    if data.lower() == 'not anonymous':
                        data = 'Anonymous'
                    writer.writerow([ip, data])
                    print(f"Scraped data for {ip}: {data}")
                    return
        except (aiohttp.ClientError, asyncio.TimeoutError):
            await asyncio.sleep(5)

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
        writer.writerow(['IP', 'Info'])
        while start_ip < 256:
            mullvad_connect()
            wait_until_vpn_connected()
            end_ip = start_ip + 18  # Processing IPs in batches of 18
            asyncio.run(fetch_all_ips(writer, start_ip, end_ip, subnet))
            print(f"Data saved to {filename} for IPs {start_ip} to {end_ip - 1}")
            start_ip = end_ip
            mullvad_disconnect()
            time.sleep(5)  # Optional: Pause before next batch
