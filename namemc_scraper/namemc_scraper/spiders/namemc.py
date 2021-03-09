import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.crawler import CrawlerProcess

class NamemcSpider(CrawlSpider):
    name = 'namemc'
    allowed_domains = ['namemc.com']
    start_urls = ['https://namemc.com/minecraft-skins/random']

    def parse_info(self, response):
        ids = response.xpath('//a[contains(@href,"/skin/")]/@href').getall() #[contains(@href,"/skin/*")]
        #match everything with <a href="/skin/*">
        parsedIds = []
        for id in ids:
            parsedIds.append(id.split("/skin/", 1)[1])
        return {"ids": parsedIds}

process = CrawlerProcess(settings={
    "FEEDS": {
        "ids.json": {"format": "json"}, #this is somehow saving the ids out??
    },
})

process.crawl(NamemcSpider)
process.start() # the script will block here until the crawling is finished

#this crawler now gets run by running the python script
#get ids back from crawler
#store ids in set > this is already ha
#save set to file