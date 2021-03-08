import scrapy


class NamemcSpider(scrapy.Spider):
    name = 'namemc'
    allowed_domains = ['namemc.com']
    start_urls = ['https://namemc.com/minecraft-skins/random']

    def parse(self, response):
        ids = response.xpath('//a[contains(@href,"/skin/")]/@href').getall() #[contains(@href,"/skin/*")]
        #match everything with <a href="/skin/*">
        parsedIds = []
        for id in ids:
            parsedIds.append(id.split("/skin/", 1)[1])
        return {"ids": parsedIds}
