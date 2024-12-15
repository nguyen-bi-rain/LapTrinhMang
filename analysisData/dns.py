import socket
import ipaddress as ip
from geoip import geolite2
import netifaces


def get_interface():
    interfaces = netifaces.interfaces()
    my_interface = {}
    for i in interfaces:
        addr = netifaces.ifaddresses(i)
        my_address = dict()
        if netifaces.AF_INET in addr.keys():
            my_address["ipv4"] = addr[netifaces.AF_INET]
        if netifaces.AF_INET6 in addr.keys():
            my_address["ipv6"] = addr[netifaces.AF_INET6]

        my_interface[i] = my_address
    return my_interface

CLASS_C = '192.168.0.0'
prefix = 24       #24-30

def subnetworth():
    net_address = CLASS_C + '/' + str(prefix)
    try:
        network = ip.ip_network(net_address)
    except:
        raise Exception("fail to create network")
    print("network configuration \n")
    print("\t network address: %s"%network.network_address)
    print("\t number address: %s"%network.num_addresses)
    print("\t netmask: %s"%network.netmask)
    print("\t netmask: %s"%network.broadcast_address)
    first_ip ,last_ip = list(network.hosts())[0],list(network.hosts())[-1]
    print("\t host ip from %s to %s"%(first_ip,last_ip))
    for sub in network.subnets(new_prefix=26):
        print(sub)
        print(sub[0])
        print(sub[-1])



def get_host_ip():
    try:
        hostname = socket.gethostname()
        hostip = socket.gethostbyname(hostname)
        print("hostname :" ,hostname)
        print("ip",hostip)
    except:
        print("khong lay dc ip")




def get_geo(ipaddress):
    reader = geolite2.reader()
    result = reader.get(ipaddress)
    if result is not None:
        print("Country: ", result['country']['iso_code'])
        print("Continent: ", result['continent']['names']['en'])
        print("Timezone: ", result['location']['time_zone'])
    geolite2.close()

# print all broadcast address
if __name__ == '__main__':
    hostname = socket.gethostname()
    hostip = socket.gethostbyname(hostname)
    get_geo(hostip)





        
# bai tap
# import googlemaps
# from datetime import datetime
# from geoip import geolite2

# gmaps = googlemaps.Client(key = '')
# taodo = gmaps.geocode('GTVT')
# reverse_geocode = gmaps.reverse_geocode(taodo)
# now = datetime.now()
# direction = gmaps.directions('hanoi','noibai',mode="transit",departure_time = )

