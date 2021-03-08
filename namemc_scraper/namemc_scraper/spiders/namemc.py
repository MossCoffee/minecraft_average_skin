import scrapy


class NamemcSpider(scrapy.Spider):
    name = 'namemc'
    allowed_domains = ['namemc.com']
    start_urls = ['https://namemc.com/minecraft-skins/random']

    def parse(self, response):
        
        pass
