import requests
from urllib.request import urlopen
import ipaddress as ip
from bs4 import BeautifulSoup


def get_info_from_a_website(url):
    headers = requests.utils.default_headers(url)
    r = requests.get(url, headers)
    bs = BeautifulSoup(r.content, 'html.parser')
    text = bs.find_all("css selector")
    for t in text:
        print(t.get_text())

def divideip(ipaddress):
    network = ip.ip_network(ipaddress)
    print(network.network_address)
    print(network.num_addresses)
    print(network.netmask)
    print(network.broadcast_address)

