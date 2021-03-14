import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.crawler import CrawlerProcess

id_dict = {}

class NamemcSpider(scrapy.Spider):
    name = 'namemc'
    allowed_domains = ['namemc.com']
    start_urls = ['https://namemc.com/minecraft-skins/random']

    def parse(self, response):
        print("parsing...")
        ids = response.xpath('//a[contains(@href,"/skin/")]/@href').getall() #[contains(@href,"/skin/*")]
        for id in ids:
            parsedID = id.split("/skin/", 1)[1]
            id_dict[parsedID] = parsedID
        return scrapy.Request("https://namemc.com/minecraft-skins/random", callback=self.reload_url, dont_filter=True)


    def reload_url(self, response):
        max_ids= 100
        if(len(id_dict) < max_ids): 
            yield self.parse(response)
        else:
            self.writeOutIDs()
            return
    
    def writeOutIDs(self):
        with open('id_file', 'w') as f:
         
         for id in id_dict:
          f.write(id + '\n')

process = CrawlerProcess(settings={
    "FEEDS": {},
})

process.crawl(NamemcSpider)
process.start()