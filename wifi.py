import pywifi
import requests
import os
import time
import logging
from requests.exceptions import RequestException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from pywifi import const
from pywifi import Profile
from pywifi import const
from hashlib import md5
from bs4 import BeautifulSoup
from config import *

ps = 1
pid = '2'
calg = '12345678'
max_count = 10
logging.basicConfig(
    level=logging.DEBUG,
    filename='wifi.log',
    datefmt='%Y/%m/%d %H:%M:%S',
    format=
    '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s'
)
logger = logging.getLogger(__name__)


def login(username, password, pattern):
    headers = {
        'Referer':
        'http://10.10.43.3/',
        'Host':
        '10.10.43.3',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.189 Safari/537.36 Vivaldi/1.95.1077.55',
        'Upgrade-Insecure-Requests':
        '1'
    }
    if pattern == 0:
        data = {
            'DDDDD': username,
            'upass': password,
            'R1': '0',
            'R2': '1',
            'para': '00',
            '0MKKey': '123456'
        }
        try:
            response = requests.post(
                'http://10.10.43.3/',
                data=data,
                headers=headers,
                allow_redirects=False)
            if response.status_code == 200:
                print('success')
        except RequestException or NewConnectionError:
            time.sleep(3)
            return login(USERNAME, password, pattern)
        except MaxRetryError:
            time.sleep(3)
            return login(USERNAME, password, pattern)
    else:
        data = {
            'DDDDD': username,
            'upass': password,
            '0MKKey': '%B5%C7%C2%BC%28Login%29',
            'C2': 'on'
        }
        try:
            response = requests.post(
                'http://10.1.61.1/a70.htm',
                data=data,
                headers=headers,
                allow_redirects=False)
            if response.status_code == 200:
                print('success')
        except RequestException or NewConnectionError:
            time.sleep(3)
            login(USERNAME, password, pattern)
        except MaxRetryError:
            time.sleep(3)
            login(USERNAME, password, pattern)


def connectWifi():
    count = 1
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    bsses = iface.scan_results()
    if bsses[0].ssid != 'local.wlan.bjtu':
        os.system("netsh wlan disconnect")

    # connect(iface)
    os.system('netsh wlan connect name=local.wlan.bjtu')
    while True:
        time.sleep(3)
        count += 1
        if count < max_count:
            response = requests.get('http://10.10.43.3')
            if response.status_code != 200:
                os.system("netsh wlan disconnect")
                os.system('netsh wlan connect name=local.wlan.bjtu')
            else:
                break
        else:
            response = requests.get('http://10.1.61.1/a70.htm')
            if response.status_code != 200:
                os.system("netsh wlan disconnect")
                os.system('netsh wlan connect name=web.wlan.bjtu')

            else:
                break
    if iface.status() in [const.IFACE_CONNECTED, const.IFACE_CONNECTING]:
        print('连接次数:', count)
        time.sleep(2)
        if count <= max_count:
            password = getPassword()
            login(USERNAME, password, 0)
        else:
            login(USERNAME, PASSWORD, 1)


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
