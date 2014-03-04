#!/usr/bin/env python 
import req_proxy
import phan_proxy
from bs4 import BeautifulSoup
import logging
import time
import multiprocessing
import phan_proxy
import urll_proxy
import os 


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 10
enclosure_queue = multiprocessing.JoinableQueue()


def main4(line, filename):
    menulink = line[0]
    menutitle  = line[1]

    driver = phan_proxy.main(menulink)

    height = 0
    loop = True

    while loop is True:
        logging.debug("scrolling...")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        heightnow = driver.execute_script("return $(document ).height();")

        if heightnow == height:
            loop = False

        else:
            height = heightnow
            loop = True

    page = driver.page_source
    
    soup = BeautifulSoup(page)

    tag_main_comp_holder = soup.find("div", attrs={"class":"campaignHolder mainCampaignHolder"})

    tag_a = tag_main_comp_holder.find_all("a", attrs={"class":"indulgeLink"})
      
    line2 = str(line).strip("[]").strip()
    
    f = open(filename, "a+")
    
    for al in tag_a:
        clink = str(al.get("href")).strip()
        catlink = "%s%s" %("http://www.fashionandyou.com", clink)
        cattitle = clink.replace("/", "").strip()
        
        print >>f, ','.join([menulink, menutitle, catlink, cattitle])
	logging.debug((line2, catlink, cattitle))
        
    f.close()




def main3(i, q):
    for line, filename in iter(q.get, None):
        #try:
        main4(line, filename)

        #except:
        #    pass

        time.sleep(2)
        q.task_done()

    q.task_done()




def main2(menucontainer):
    procs = []

    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_ml_mt_cl_ct.txt")

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=main3, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for line in menucontainer:
        enclosure_queue.put((line, filename))

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()

    
    print "Finished everything...."
    print "num active children:", multiprocessing.active_children()
    
    print "closing the file..."



def main():

    directory = "dir%s" %(time.strftime("%d%m%Y"))
    
    try:
        os.makedirs(directory)
    except:
        pass

    f = open("to_extract.txt", "w+")
    print >>f, directory
    f.close()

    f = open("extracted.txt", "a+")
    print >>f, directory
    f.close()

    link = "http://www.fashionandyou.com/"
    #page = req_proxy.main(link)
    page = urll_proxy.main(link)
    
    soup = BeautifulSoup(page)
     
    tag_menu = soup.find("ul", attrs={"id":"verticalsMenu"})

    tag_menu_li = tag_menu.find_all("a", attrs={"class":"vertical-tab"})

    menucontainer  = []

    for al in tag_menu_li:
        menulink =  "%s%s" %("http://www.fashionandyou.com", str(al.get("href")).strip())
        menutitle = str(al.get_text())
 
        menucontainer.append([menulink, menutitle])

    main2(menucontainer)
    
        

  


if __name__=="__main__":
    main()
        


    

