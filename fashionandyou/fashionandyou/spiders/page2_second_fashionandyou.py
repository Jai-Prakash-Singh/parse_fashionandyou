import phan_proxy
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import re
import logging
import time
import multiprocessing
import os



logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 20
enclosure_queue = multiprocessing.JoinableQueue()




def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")

    except WebDriverException:
        pass




def sub_cat_select(driver, sub_cat):
    select = Select(driver.find_element_by_id("categorySelect"))

    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
    except WebDriverException:
        pass

    select.select_by_visible_text(sub_cat)
   
    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
    except WebDriverException:
        pass

    return driver




def driver_scroller(driver):
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

    return driver




def main(line):
    line2 = line.strip().split(",")
    sub_cat = line2[-1].strip()

    cattitle = line2[-2].strip()
    catlink = line2[-3].strip()

    menutitle = line2[1].strip()
    menulink =  line2[0].strip()

    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    if sub_cat  ==  "None":
        sub_cat2 = cattitle
        sub_dir =  "%s/%s/%s/%s" %(directory, menutitle, cattitle, sub_cat2)
        filename1 =  "%s/%s.doc" %(sub_dir,sub_cat2)
	filename2 = "%s/%s.docx" %(sub_dir,sub_cat2)

    else:
        sub_dir =  "%s/%s/%s/%s" %(directory, menutitle, cattitle, sub_cat)
	filename1 =  "%s/%s.doc" %(sub_dir,sub_cat)
	filename2 = "%s/%s.docx" %(sub_dir,sub_cat)

    try:
        os.makedirs(sub_dir)

    except:
        pass

    f = open(filename1, "a+")
    f2 = open(filename2, "a+")
   
    driver = phan_proxy.main(catlink)

    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
    except WebDriverException:
        pass

    if (sub_cat != "None") and (sub_cat != "All Categories") :
        driver = sub_cat_select(driver, sub_cat)
    
    driver = driver_scroller(driver)
        
    page = driver.page_source

    soup = BeautifulSoup(page)

    tag_ul_product = soup.find("ul", attrs={"class":"products"})

    tag_li_dis_block = tag_ul_product.find_all("li", attrs={"style" : re.compile(": block;")})

    for al in tag_li_dis_block:
        tag_al_a = al.find("a", attrs={"class":"productLink"})

	if tag_al_a:
            productlink = "%s%s" %("http://www.fashionandyou.com", str(tag_al_a.get("href")).strip())
            print >>f,  ','.join([menulink, menutitle, catlink, cattitle, sub_cat,  productlink])
	    print >>f2 , productlink

	    logging.debug([menulink, menutitle, catlink, cattitle, sub_cat,  productlink])

    print len(tag_li_dis_block)

    driver.delete_all_cookies()
    driver.quit()
    f.close()
    f2.close()
    


def supermain2(i, q):
    for line in iter(q.get, None):
        try:
            main(line)
        except:
            pass
        line = line.strip()
	 
	print line

	time.sleep(2)
	q.task_done()

    q.task_done()


def supermain():
    f = open("to_extract.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_ml_mt_cl_ct_sct.txt")
    
    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=supermain2, args=(i, enclosure_queue,)))
	#worker.setDaemon(True)
	procs[-1].start()

    for line in f:
        enclosure_queue.put(line)

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
    line = "http://www.fashionandyou.com/women,women,http://www.fashionandyou.com/all-about-perfumes,all-about-perfumes,Men EDT"
    #main(line)   
    supermain() 

    
