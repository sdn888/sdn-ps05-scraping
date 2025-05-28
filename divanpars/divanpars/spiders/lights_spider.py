import scrapy

class LightsSpider(scrapy.Spider):
    name = "lights"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        products = response.css('div.LlPhw')

        for product in products:
            name = product.css('span[itemprop="name"]::text').get()
            price = product.css('meta[itemprop="price"]::attr(content)').get()
            relative_url = product.css('a::attr(href)').get()
            full_url = response.urljoin(relative_url)

            if name and price and relative_url:
                yield {
                    "name": name.strip(),
                    "price": price.strip(),
                    "url": full_url
                }

        # Переход на следующую страницу
        next_page = response.css('a.Pagination-module__paginationButton--BEO2J[aria-label="Следующая страница"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
