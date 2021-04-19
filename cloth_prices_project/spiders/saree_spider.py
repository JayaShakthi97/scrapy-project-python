import scrapy
from scrapy.loader import ItemLoader
from cloth_prices_project.items import ClothItem


class SareeSpider(scrapy.Spider):
    # identity
    name = "sareespider"

    # request
    def start_requests(self):
        # first page url
        url = 'https://www.fashionbug.lk/product-category/women/saree'

        yield scrapy.Request(url=url, callback=self.parse)

    # response
    def parse(self, response):
        for saree in response.selector.xpath("//li[contains(@class, 'product type-product')]"):
            loader = ItemLoader(item=ClothItem(), selector=saree, response=response)
            loader.add_xpath('title', ".//h2[@class='woocommerce-loop-product__title']/text()")
            loader.add_xpath('price', ".//span[@class='woocommerce-Price-amount amount']/text()")
            loader.add_xpath('img_url', ".//img[@class='attachment-woocommerce_thumbnail size-woocommerce_thumbnail']/@src")
            yield loader.load_item()

        # get next pages urls
        next_page_url = response.selector.xpath("//a[@class='next page-numbers']/@href").extract_first()
        # call parse method for each pages
        if next_page_url is not None:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
            