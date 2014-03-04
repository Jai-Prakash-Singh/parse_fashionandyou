#!/usr/bin/env python 
import logging
import req_proxy
from bs4 import BeautifulSoup
import multiprocessing
import time 

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 10
enclosure_queue = multiprocessing.JoinableQueue()




def main3(line, f2):
    line = line.strip()
    line2 = line.split(",")
    catlink = line2[-2]
   
    page = req_proxy.main(catlink)
    
    soup = BeautifulSoup(page)

    subcat = soup.find("select", attrs={"id":"categorySelect"})
    
    try:
        subcatoption =  subcat.find_all("option")

        for subcatop in subcatoption:
            print >>f2, "%s,%s" %(line , str(subcatop.get_text()).strip())

            logging.debug("%s,%s" %(line , str(subcatop.get_text()).strip()))

    except:
        print >>f2, "%s,%s" %(line , "None")

        logging.debug("%s,%s" %(line, "None"))




def main2(i, q):
    for line , filename2 in iter(q.get, None):
        f2 = open(filename2, "a+")
        main3(line, f2)
        f2.close()

	time.sleep(2)
	q.task_done()
    
    q.task_done()




def main():        
    procs = []

    f = open("to_extract.txt")
    directory = f.read().strip() 
    f.close()

    filename = "%s/%s" %(directory, "f_ml_mt_cl_ct.txt")

    filename2 = "%s/%s" %(directory, "f_ml_mt_cl_ct_sct.txt")

    f = open(filename)

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=main2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for line in f:
        enclosure_queue.put((line, filename2))

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

    f.close()




if __name__=="__main__":
    line = "http://www.fashionandyou.com/all-sales,All Sales,http://www.fashionandyou.com/dress-the-diva,dress-the-diva"
    #main3(line)
    main()

