import scrapy

from scrapy.loader import ItemLoader

from ..items import SozialbankdeItem
from itemloaders.processors import TakeFirst


class SozialbankdeSpider(scrapy.Spider):
	name = 'sozialbankde'
	start_urls = ['https://www.sozialbank.de/news-events/news/news']

	def parse(self, response):
		post_links = response.xpath('//*[(@id = "main_content")]//div[contains(@class, "frame")][p]')
		for post in post_links:
			title = post.xpath('./h2/text()').get()
			description = post.xpath('./p[position()>1]/text()').get()
			date = post.xpath('./p/text()').get()

			item = ItemLoader(item=SozialbankdeItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
