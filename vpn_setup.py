#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import sys
import os

from collections import namedtuple
Vpn_hosts = namedtuple('Vpn_hosts', 'country delay url')
host_url =  "http://www.vpngate.net"
url = "http://www.vpngate.net/en/"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

print "visiting " + host_url + " ..."
data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
page = response.read()

soup = BeautifulSoup(page)
tables = soup.find_all('table', id="vg_hosts_table_id")
vpn_tuples= []
for table in tables:
    soup_table = BeautifulSoup(str(table))
    table_cols = soup_table.find_all('tr')
    if len(table_cols) > 20:
        break

for col in table_cols:
    delay = re.findall(r'(\d+)\sms', str(col))
    if len(delay) == 0: #not a valid column
           continue 
    country = re.findall(r'<br/>([A-Z].+)</td><td class="vg_table_row_[0-9]">', str(col))
    url_c = re.findall(r'href="(do_openvpn.+\d+)"><img\sheight="\d+"', str(col))
    '''
    print country
    print delay
    print url_c
    '''
    if len(url_c) !=0:
        vpn_tuples.append(Vpn_hosts(country[0], int(delay[0]), url_c[0]))

#sort and find the minimum ping delay
vpn_tuples = sorted(vpn_tuples, key=lambda host: host.delay)
'''
for v in vpn_tuples:
    print v
'''
if len(vpn_tuples) == 0:
    print 'fail to access website'
    sys.exit(1)
else:    
    navi_url = url + vpn_tuples[0].url
    navi_url = navi_url.replace("&amp;", "&")
    print "Connecting to "+ vpn_tuples[0].country + " VPN with ping delay " +  str(vpn_tuples[0].delay) +"ms"
    #print  navi_url


#navigate to the page where to download the .ovpn file
req = urllib2.Request(navi_url, data, headers)
response = urllib2.urlopen(req)
page = response.read()
soup = BeautifulSoup(page)
download_links = soup.find_all('a')
vpn_file_urls = re.findall(r'href="(.+\.ovpn)',str(download_links))
if len(vpn_file_urls) != 0:
    #print vpn_file_urls
    i = 0
    for urls in vpn_file_urls:
        vpn_file_urls[i] = urls.replace("&amp;", "&")
        #print vpn_file_urls[i]
        i +=1
    ovpn_file_url = host_url + vpn_file_urls[0]
    #print ovpn_file_url
    download_path = "/tmp/"
    downloaded_file_name  = str(vpn_tuples[0].country).replace(" ","")+"_" + str(vpn_tuples[0].delay)+"ms.ovpn"
    print "config file " + downloaded_file_name + " downloaded at /tmp/" 
    urllib.urlretrieve(ovpn_file_url, download_path+downloaded_file_name)
    print "need sudo to run openvpn"
    os.system("sudo openvpn --config " + download_path + downloaded_file_name)

else:
    print "no ovpn file found"
    sys.exit(1)
    
