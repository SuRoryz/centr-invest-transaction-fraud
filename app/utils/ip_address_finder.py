from urllib.request import urlopen
import json

def print_ip_info(addr=None):
    if addr is None:
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'

    res = urlopen(url)
    data = json.load(res)
    
    return data