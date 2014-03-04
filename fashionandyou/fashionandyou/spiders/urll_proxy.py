import random
import  urllib2
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)




def main(url):
    #f = open("/home/desktop/proxy_http_auth.txt")
    f = open("/home/user/Desktop/proxy_http_auth.txt")
    file_pass_ip = f.read().strip().split('\n')
    f.close()

        
    for i in xrange(5):
        try:
            pass_ip = random.choice(file_pass_ip).strip()
            logging.debug(pass_ip)
            proxy = urllib2.ProxyHandler({'http': 'http://'+pass_ip})
            auth = urllib2.HTTPBasicAuthHandler()
            opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            conn = urllib2.urlopen(url)
            page = conn.read()
            conn.close()
            return page 
        except:
            pass

    return None



if __name__=="__main__":
    page  = main("http://python.org")
    print page
