# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join

def remove_charater(value):
    return float(value.replace(u"\u00a0", '').replace(',', ''))

class ClothItem(scrapy.Item):
    title = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(remove_charater),
        output_processor = TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor = TakeFirst()
    )
