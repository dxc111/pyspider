import scrapy,os, sys,time
from scpider.items import PeopleItem


class PeopleSpider(scrapy.Spider):
    name = 'people'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    start_urls = [
        'https://www.goodreads.com/quotes?page=2',
        'https://www.goodreads.com/quotes?page=3',
        'https://www.goodreads.com/quotes?page=4'
    ]
    count = 0
    def parse(self, response):
        imgs = response.xpath("//a[@class='leftAlignedImage']/img/@src").extract()
        names = response.xpath("//a[@class='leftAlignedImage']/img/@alt").extract()
        contents = response.xpath("//div[@class='quoteText']/text()").re('“(.*)”')
        with open('Says.text', 'w+') as f:
            for index, img in enumerate(imgs):
                name = names[index][:10].strip()
                content = contents[index].strip()
                # print('%s said: %s' %(name, content))s
                f.write('%s said: %s\n' %(name, content))
                time.sleep(2)
                yield scrapy.Request(img, lambda response, name=name : self.save_img(response, name))

        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     yield scrapy.follow(next_page, callback=self.parse)

    def save_img(self, response, name):
        self.count += 1
        print(self.count)
        if not os.path.exists('./people'):
            os.mkdir('./people')
        with open('./people/' + name+'.jpg', 'wb') as f:
            f.write(response.body)
