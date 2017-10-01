import scrapy
from ..items import GjirafaComItem


class GetDataSpider(scrapy.Spider):
    name = 'gjirafa'
    allowed_domains = ['gjirafa.com']
    start_urls = ['https://gjirafa.com/Top/Patundshmeri?f=0']
    page = 0

    def parse(self, response):
        next_page = response.xpath('//p[@class="pag_btn curr_pag_btn"]/following-sibling::button').extract_first()

        if next_page:
            self.page += 1
            yield scrapy.Request('%s%s' % (self.start_urls[0][:-1], self.page), callback=self.parse)

        urls = response.xpath('//h3/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)

    @staticmethod
    def decode_cfemail(cfemail):
        row = int(cfemail[:2], 16)
        email = ''.join([chr(int(cfemail[i:i + 2], 16) ^ row) for i in range(2, len(cfemail), 2)])
        return email

    def parse_item(self, response):
        no_data = '-'
        item = GjirafaComItem()
        try:
            dirty_email = response.xpath('//span[@class="__cf_email__"]/@data-cfemail').extract_first()
        except:
            dirty_email = ''
        item['email'] = self.decode_cfemail(dirty_email) if dirty_email else no_data
        try:
            item['phone'] = response.xpath('//a[@class="clickCall"]/text()').extract_first()
        except:
            item['phone'] = no_data
        try:
            item['location'] = response.xpath('//h4/text()').extract_first()
        except:
            item['location'] = no_data
        yield item
