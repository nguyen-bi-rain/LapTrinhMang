from urllib.request import urlopen
from urllib.request import Request


if __name__ == '__main__':
    r = Request("https://en.wikipedia.org/wiki/Python")
    res = urlopen(r)
    print(res.getheader('server'))