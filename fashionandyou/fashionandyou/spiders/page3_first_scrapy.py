# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import time
from lxml import html
import re

#page3_scrapy_myntra.py , page3_filedivision_myntra.py 

class DmozSpider(BaseSpider):
    name = "link_to_link"
    allowed_domains = ["fashionandyou.com"]

    def __init__(self, pth = None):
        pthdoc = pth.strip()[:-1]

        pth2 = str(pth).strip().split("/")

        f = open(pthdoc)
        line = f.readline().strip()
        f.close()

        linelist = line.split(",")
        self.subcat = linelist[-2]

        self.catlink = linelist[2]

        self.pth = pth
        self.pth2 = pth2

        self.target = str(linelist[1]).strip()

        category = str(linelist[3]).strip()
        self.category = category

        f = open(pth)
        avalurls = f.read().strip().split("\n")
        self.start_urls = map(str.strip, avalurls)
        f.close()
    

    def parse(self, response):
        #try:
            link = response.url

            page = response.body

            soup = BeautifulSoup(page)
             
            tree = html.fromstring(page)
             
            title = tree.xpath("/html/body/div[2]/div/div/div[5]/h5/text()")
            title = str(title[0]).strip()
            
            sp = soup.find("span", attrs={"class":"newPrice"})
            sp = str(sp.get_text()).strip()

            mrp = soup.find("span", attrs={"class":"oldPrice"})

            if mrp:
                mrp = str(mrp.get_text()).strip()

            else:
                mrp = sp

            size_cont = []
            
            try:
                size = soup.find("select", attrs={"id":"productVariants"})
                size_option = size.find_all("option")
                size_option = size_option[1:]
                
		for sz in size_option:
                    sz2 = str(sz.get_text()).replace("\n", " ").replace("\r", " ").replace("\t", " ").replace(",", " ").strip()
		    size_cont.append(sz2)

		size = str(size_cont)

            except:
                size = "None"

            vender = "fashionandyou.com"

            tag_desc = soup.find("div", attrs={"class":"product_desc"})
            spec = str(tag_desc).replace("\n", " ").replace("\r", " ").replace("\t", " ")

            brand = "None"
            tag_brand = tag_desc.find("strong", text = re.compile("BRAND"))

            if tag_brand:
                brand = str(tag_brand.next_sibling).strip()
  

            sku = "None"
            tag_sku = tag_desc.find("strong", text = re.compile("PRODUCT CODE"))

            if tag_sku:
                sku  = str(tag_sku.next_sibling).strip()

            image = soup.find("img", attrs={"id":"myimage"})
            image = str(image.get("src"))

            colour = "None"
            tag_colour = tag_desc.find("strong", text = re.compile("COLOUR"))

            if tag_colour:
                colour = str(tag_colour.next_sibling).strip()


            desc = "None"

            target = self.target
            category = self.category
            subcat  = self.subcat
            
            metatitle = "None"
            metadisc = "None"

            catlink = self.catlink

            date = str(time.strftime("%d:%m:%Y"))
            status = "None"

            directory = '/'.join(self.pth2[:-1])

            filename = "%s/%s%s" %(directory , self.pth2[-1][:-5],  ".csv")

            f = open(filename, "a+")
            print>>f,  ','.join([sku, title, catlink, sp, category, subcat, brand, image, mrp,
                        colour, target, link, vender, metatitle, metadisc, size,
                        desc, spec, date, status])

            print [sku, title, catlink, sp, category, subcat, brand, image, mrp,
                        colour, target, link, vender, metatitle, metadisc, size,
                        desc, spec, date, status]
            f.close()

            print[link, "ok"]


        #except:
        #   f = open("to_scrape_once_again", "a+")
        #   print >>f, str(self.pth), str(response.url)
        #   f.close()
        #   self.start_urls.append(str(response.url))
