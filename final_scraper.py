import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import scrapy_xlsx

itemList=[]
class plateScraper(scrapy.Spider):
    name = 'scrapePlate'
    allowed_domains = ['dvlaregistrations.dvla.gov.uk']
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'output_r00.xlsx','DOWNLOAD_DELAY': .001, 'LOG_LEVEL':'INFO'}

    def start_requests(self):
        df=pd.read_excel('data.xlsx')
        columnA_values=df['PLATE']
        for row in columnA_values:
            global  plate_num_xlsx
            plate_num_xlsx=row
            base_url =f"https://dvlaregistrations.dvla.gov.uk/search/results.html?search={plate_num_xlsx}&action=index&pricefrom=0&priceto=&prefixmatches=&currentmatches=&limitprefix=&limitcurrent=&limitauction=&searched=true&openoption=&language=en&prefix2=Search&super=&super_pricefrom=&super_priceto="
            url=base_url
            yield scrapy.Request(url,callback=self.parse, cb_kwargs={'plate_num_xlsx': plate_num_xlsx})

    def parse(self, response, plate_num_xlsx=None):
        plate = response.xpath('//div[@class="resultsstrip"]/a/text()').extract_first()
        price = response.xpath('//div[@class="resultsstrip"]/p/text()').extract_first()

        try:
            a = plate.replace(" ", "").strip()
            if plate_num_xlsx == plate.replace(" ", "").strip():
                item = {"plate": plate_num_xlsx, "price": price.strip()}
                itemList.append(item)
                print(item)
                yield item
            else:
                item = {"plate": plate_num_xlsx, "price": "-"}
                itemList.append(item)
                print(item)
                yield item
        except:
            item = {"plate": plate_num_xlsx, "price": "-"}
            itemList.append(item)
            print(item)
            yield item

process = CrawlerProcess()
process.crawl(plateScraper)
process.start()

import winsound
winsound.Beep(555,333)