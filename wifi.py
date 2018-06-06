import pywifi
import requests
import os
import time
from requests.exceptions import RequestException
from pywifi import const
from pywifi import Profile
from pywifi import const
from hashlib import md5
from bs4 import BeautifulSoup
from config import *


ps = 1
pid = '2'
calg = '12345678'


def login(username, password):
    headers = {
        'Referer': 'http://10.10.43.3/',
        'Host': '10.10.43.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.189 Safari/537.36 Vivaldi/1.95.1077.55',
        'Upgrade-Insecure-Requests': '1'
    }
    data = {
        'DDDDD': username,
        'upass': password,
        'R1': '0',
        'R2': '1',
        'para': '00',
        '0MKKey': '123456'
    }
    try:
        response = requests.post('http://10.10.43.3/',
                                 data=data, headers=headers, allow_redirects=False)
    except Exception:
        login(USERNAME, password)


def connectWifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    bsses = iface.scan_results()
    if bsses[0].ssid != 'local.wlan.bjtu':
        os.system("netsh wlan disconnect")
        time.sleep(1)
    # connect(iface)
    while True:
        os.system('netsh wlan connect name=local.wlan.bjtu')
        status = os.system('ping -c 1 10.10.43.3')
        if status == 1:
            os.system('netsh wlan connect name=local.wlan.bjtu')
        else:
            break
    if iface.status() in [const.IFACE_CONNECTED]:
        username = '16301                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 164'
        password = getPassword()
        login(USERNAME, password)


def connect(iface):
    profile = pywifi.Profile()
    profile.ssid = 'local.wlan.bjtu'
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)
    profile.cipher = const.CIPHER_TYPE_NONE
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    if iface.status() not in [const.IFACE_CONNECTED]:
        connect(iface)


def getPassword():
    response = requests.get('http://10.10.43.3/md5calg')
    soup = BeautifulSoup(response.text, 'lxml')
    md5clag = soup.find('body').text
    md5clag = md5clag[-10:-2]
    origin = PASSWORD
    tmpchar = pid + origin + md5clag
    btmpchar = bytes(tmpchar, encoding='utf-8')
    password = md5(btmpchar).hexdigest() + md5clag + pid
    return password


def main():
    connectWifi()


if __name__ == '__main__':
    main()
