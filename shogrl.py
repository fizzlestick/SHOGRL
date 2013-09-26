#!/usr/bin/python
#########################################################################
#   ___  _   _  _____  ___  ____  __
#  / __)( )_( )(  _  )/ __)(  _ \(  )
#  \__ \ ) _ (  )(_)( ( (_-.)   / )(__
#  (___/(_) (_)(_____)\___/(_)\_)(____) V0.2
# -some code borrowed from >> https://developers.shodan.io/index.html
# -rest created/mixed up by FIZZLESTICK
# -trollsohard[at]rebelbas.es
#
# MORE INFO COMING
#
# [changelog]
# 9/25/2013 v0.2 - written up for RC worth.. needs some IP/vs DNS handling
# next
#########################################################################

import shodan
import sys
from shodan import WebAPI

mykey = "INSERTYOURWEBAPIKEYHERETHELONGSTRING"
api = WebAPI(mykey)
apinfo = api.info()

from scapy.all import *
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb=0

def shosearch(crap):
    try:
        results = api.search(derpstring, limit=None)
        print '[*] TOTAL # OF HITS: %s' % results['total']
    except Exception, e:
        print '[ERROR:] %s' % e

def probe():
    myprobe = (IP(dst='www.shodanhq.com')/TCP(dport=80,flags="S"))
    try:
        derp = sr1(myprobe, timeout=1)
        derpy = derp.summary()
        if derpy.find('SA') != -1:
            print "SHODAN UP"
    except Exception, ack:
        print 'SHODAN DOWN FOR SOME REASON.. EXITING....'
        sys.exit()

def shohost(crap):
    host = api.host(derpstring)
    try:
        print '----------------------------------------------------------------------'
        print '[*] IP ADDRESS: ',host.get('ip')
        print '[*] Operating System: ',host.get('os')
        print '[*] Hostnames: ',host.get('hostnames')
        print '[*] Country: ',host.get('country_code')
        print '[*] Region: ',host.get('region_name')
        print '[*] City: ',host.get('city')
        print '[*] Latitude: ',host.get('latitude')
        print '[*] Longitude: ',host.get('longitude')
        print '----------------------------------------------------------------------'
        for item in host['data']:
            print '-- TIMESTAMP\t\t',item['timestamp']
            print '-- PORT\t\t\t\t',item['port']
            print '-- BANNER\t\t\t',item['banner'],
    except Exception, e:
        print '[ERROR:] %s' % e

def sholist(crap):
    try:
        api = shodan.WebAPI(mykey)
        query = derpstring
        #listpage = raw_input('<Which page?> ')
        #listlimit = raw_input('<Result limit?> ')
        #result = api.search(query, page=listpage, limit=listlimit)
        result = api.search(query)
        print '----------------------------------------------------------------------'
        print '| [Total Hits:] %s' % result['total']
        print '| Top Countries'
        for places in result['countries']:
            print '|\t\t',places['name'],places['count']
        print '-[CSV BELOW]----------------------------------------------------------'
        for host in result['matches']:
            print host['ip']+','+host['country_name']+','+host['isp']
    except Exception, e:
        print 'Error: %s' % e
        sys.exit(1)

#SHO-TIME
probe()
print '======================================================================'
print ' ______     __  __     ______     ______     ______     __ '
print "/\  ___\   /\ \_\ \   /\  __ \   /\  ___\   /\  == \   /\ \ "
print '\ \___  \  \ \  __ \  \ \ \/\ \  \ \ \__ \  \ \  __<   \ \ \____ '
print ' \/\_____\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_____\ '
print '  \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_/ /_/   \/_____/ '
print ' ... a shodan search utility...:: PROTOTYPE v0.2 :: FIZZLE.. .   .    .        .'
print '======================================================================'
print '[FILTERS:] OS/PORT/GEO/HOSTNAME'
print '[PREMIUM:] NET/CITY/COUNTRY/BEFORE/AFTER/LIMIT/PAGE'
print '[BOOLEAN:] "+" "-" and "|" to include and exclude terms'
print '[ACCOUNT:]', apinfo.get('unlocked_left'),'unlocked queries remain this month'
print '----------------------------------------------------------------------'
print '<Example1:> xampp port:8080      #XAMPP on 8080 port'
print '<Example2:> apache os:linux      #APACHE on linux'
print '<Example3:> hostname:secret      #records with hostname secret'
operr = raw_input('[*] (S)earchtotal (H)ostinfo or (L)istcreate ? >> ').lower()
derpstring = raw_input('[*] SEARCH STRING PLEASE >> ')
if operr == 's':
    print '[*] Searching Shodan........'
    shosearch(derpstring)
elif operr == 'h':
    print '[*] Host information...'
    shohost(derpstring)
elif  operr == 'l':
    print '[*] List out to CSV.....'
    yourlist = sholist(derpstring)
    print yourlist
print '----------------------------------------------------------------------'
print '..<< shes giving you all shes got captain!!!! <<'
exit()
