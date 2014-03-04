import base64
from random import choice
import subprocess
import sys
import os
import time

#f = open("/home/desktop/proxy5")
f = open("/home/user/Desktop/proxy5")
ip_list = f.read().strip().split("\n")
f.close()


class ProxyMiddleware(object):
    def process_request(self, request, spider):

        ip_port = choice(ip_list).strip()
        #print "my" , str(ip_port)
        print "*"*145
        print "myproxy: ", str(ip_port)

        request.meta['proxy'] = "http://"+ip_port
        proxy_user_pass = user_pass = "vinku:india123"
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

