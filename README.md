vpn_auto_connect for Linux
================
This python script trys to automatically connect you to the fastest VPN server
The servers chosen from http://www.vpngate.net  
The vpn servers are completely free, but they only have limited time



You need the following dependencys:
================
  BeautifulSoup
  urllib2
  urllib
  openvpn

To install them:

sudo pip install urllib

sudo pip install urllib2

sudo pip install beautidulsoup4

sudo apt-get install openvpn


To run this program:
==================
open one terminal and type:

python ./vpn_setup.py


press CTRL-C to terminate the connection


Drouble Shooting:
=================
if it prints "Initialization Sequence Completed" in the end, meaning connected successfully, otherwise there might be problem regarding firewall 
