import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from cloth_prices_project.items import ClothItem


class FashionbugSpider(CrawlSpider):
    name = 'fashionbug'
    allowed_domains = ['www.fashionbug.lk']
    start_urls = ['https://www.fashionbug.lk']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='item']/a"),
            callback='parse_item',
            follow=True
        ),
        Rule(LinkExtractor(
            restrict_xpaths="//a[@class='next page-numbers']"),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        for saree in response.selector.xpath("//li[contains(@class, 'product type-product')]"):
            loader = ItemLoader(
                item=ClothItem(), selector=saree, response=response)
            loader.add_xpath(
                'title',
                ".//h2[@class='woocommerce-loop-product__title']/text()")
            loader.add_xpath(
                'price',
                ".//span[@class='woocommerce-Price-amount amount']/text()")
            loader.add_xpath(
                'img_url',
                ".//img[@class='attachment-woocommerce_thumbnail size-woocommerce_thumbnail']/@src")
            loader.add_xpath(
                'category', "//h1[@class='woocommerce-products-header__title page-title']/text()")
            yield loader.load_item()
