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
        ids = response.xpath('//a[contains(@href,"/skin/")]/@href').getall() #[contains(@href,"/skin/*")]
        #match everything with <a href="/skin/*">
        parsedIds = []
        for id in ids:
            parsedID = id.split("/skin/", 1)[1]
            #print(parsedID)
            #parsedIds.append(parsedID)
            id_dict[parsedID] = parsedID
        return {"ids": parsedIds}

process = CrawlerProcess(settings={
    "FEEDS": {
        "ids.json": {"format": "json"}, #this is somehow saving the ids out??
    },
})

process.crawl(NamemcSpider)
for x in range(2):
    process.start() # the script will block here until the crawling is finished

with open('id_file', 'w') as f:
    for id in id_dict:
        f.write(id + '\n')

#this crawler now gets run by running the python script
#get ids back from crawler
#store ids in set > this is already happening
#save set to file