import urllib.request

"""" download a object.
print("starting download...")
url = ""
urllib.request.urlretrieve(url,"python.png");
with urllib.request.urlopen(url) as r:
    print("status : ", r.status)
    print("downloading python.org ")
    with open("python.org", "wb") as image:
        image.write(r.read())
"""

import requests, json
from urllib.request import urlopen
from bs4 import BeautifulSoup


# r = requests.get(url,{"q": "tiger","colors" : "red",'order' :'popular',})
# print(r.json())
def get_link_with_beautifulsoup():
    url = urlopen("https://en.wikipedia.org/wiki/Python")
    bs = BeautifulSoup(url)

    img = bs.find_all("img")

    for src in img:
        if 'src' in src.attrs:
            print(src.attrs['src'])
    print(len(img))


def get_link_image_with_request():
    url = "https://en.wikipedia.org/wiki/Python"
    headers = requests.utils.default_headers()
    r = requests.get(url, headers)
    bs = BeautifulSoup(r.content, "html.parser")
    images = bs.find_all("img")
    for i in images:
        print(i['src'])


# get weather of seven day
def get_weather():
    url = "https://en.wikipedia.org/wiki/Python"
    headers = requests.utils.default_headers()
    r = requests.get(url, headers)
    bs = BeautifulSoup(r.content, "html.parser")

    week = bs.find(id="seven_day_forecast")
    w = bs.find_all(class_="tombstone_container")
    d = []
    for i in range(len(w) - 1):
        period = w[i].find(class_="period_name").get_text()
        short_desc = w[i].find(class_='short_desc').get_text()
        temp = w[i].find(class_='temp').get_text()
        img = w[i].find("img")['title']
        d.append((period, short_desc, temp, img))
    for i in range(len(d) - 1):
        print(d[i])


def get_data_weather_forcast():
    url = 'https://forecast.weather.gov/MapClick.php?lat=40.7130466&lon=-74.0072301'
    headers = requests.utils.default_headers()
    response = requests.get(url, headers)
    bs = BeautifulSoup(response.content, 'html.parser')

    week = bs.find(id='seven-day-forecast')
    w = week.find_all(class_='tombstone-container')
    d = []
    for i in range(len(w) - 1):
        period = w[i].find(class_='period-name').get_text()
        short_decs = w[i].find(class_='short-desc').get_text()
        temp = w[i].find(class_='temp').get_text()
        img = w[i].find('img')['title']
        d.append((period, short_decs, temp, img))

    for i in range(len(d) - 1):
        print(d[i])


def get_data_email(url):
    headers = requests.utils.default_headers()
    response = requests.get(url, headers)
    if response.status_code == 200:
        bs = BeautifulSoup(response.content, "html.parser")
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}'
        list_email = bs.find_all(email_pattern, response)
        # loc cai trung nhau
        # loc_email = set(emails)
        return list_email
    return 0


def get_some(url):
    r = requests.get(url)
    print("HTTP status code ", str(r.status_code))
    print(r.headers)
    if r.status_code == 200:
        data = r.json()
        for d in data.items():
            print(d)
        print("header response")
        for header,value in r.headers.items():
            print(header ,"-->",value)
        print("header request")
        for header,value in r.request.headers.items():
            print(header,"-->",value)
        print("server: "+r.headers['servers'])
    else:
        print("error %s"%r.status_code)


def get_ipaddress_through_API(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        geo_info = r.json()
        print("Ip address: ",geo_info.get('ip'))
        print("Country: ",geo_info.get("country"))
        print("Region: ",geo_info.get("region"))
        print("city: ",geo_info.get("city"))
        print("location: ",geo_info.get("loc"))

        # print("Latitude: ",geo_info.get("latitude"))
        # print("Longitude: ",geo_info.get("longitude"))
    except requests.RequestException as e:
        print(f"error {e}")

def get_weather_data_api(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        weather = data['list']
        for d in weather:
            print(d['main'],d['weather'],d['clouds'],d['wind'],d['visibility'])
    except requests.RequestException as ex:
        print(ex)


if __name__ == "__main__":

    url = "https://api.openweathermap.org/data/2.5/forecast?lat=44.34&lon=10.99&appid=5e450a9f31689e58efdc5ffbd4010b61"
    get_weather_data_api(url)
    pass
