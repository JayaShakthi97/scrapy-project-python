import scrapy

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
            yield {
                'title': saree.xpath(".//h2[@class='woocommerce-loop-product__title']/text()").extract_first(),
                'price': saree.xpath(".//span[@class='woocommerce-Price-amount amount']/text()").extract_first(),
                'img_url': saree.xpath(".//img[@class='attachment-woocommerce_thumbnail size-woocommerce_thumbnail']/@src").extract_first()
            }

        # get next pages urls
        next_page_url = response.selector.xpath("//a[@class='next page-numbers']/@href").extract_first()
        # call parse method for each pages
        if next_page_url is not None:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
            