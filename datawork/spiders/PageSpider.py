import scrapy
from datawork.items import PageItem
from urllib3.util import Url, parse_url


class PageSpider(scrapy.Spider):
    name = "pageSpider"
    allowed_domains = ['financeun.com', '21so.com', 'afinance.cn', '10jqka.com.cn', 'zqcn.com.cn', 'chinavalue.net',
                       'eeo.com.cn', 'ce.cn',
                       'jrj.com.cn', 'cnfol.com', 'nbd.com.cn', 'sinoins.com']

    # 请求入口
    def start_requests(self):
        # 将 request 请求交给 调度器 schedular
        yield scrapy.Request('http://www.financeun.com/', callback=self.parse)

    # 解析函数
    def parse(self, response):
        # response 来自载器downloader
        title = response.selector.xpath('//head//title/text()').extract()
        keywords = response.xpath('//head/meta[@name="keywords"]/@content').extract()
        description = response.xpath('//head/meta[@name="description"]/@content').extract()
        all_hrefs = response.xpath('//body//@href').extract()
        content = response.xpath('//html').extract()
        item = PageItem()
        item['url'] = response.url
        item['local_urls_set'] = set()
        item['external_urls_set'] = set()
        if len(title) >= 1:
            item['title'] = title[0]
        else:
            item['title'] = 'None'
        if len(keywords) >= 1:
            item['keywords'] = keywords[0]
        else:
            item['keywords'] = 'None'
        if len(description) >= 1:
            item['description'] = description[0]
        else:
            item['description'] = 'None'
        if len(content) >= 1:
            item['content'] = content[0]
        else:
            item['content'] = 'None'
        for href in all_hrefs:
            if href.startswith('/'):
                url = parse_url(response.url)
                item['local_urls_set'].add(url.scheme + '://' + url.netloc + href)
                item['host'] = url.host
                item['file'] = '_'.join(url.path.split('/')[1:]) + '.txt'
            if href.startswith('http'):
                item['external_urls_set'].add(href)
        yield item
        for url in item['external_urls_set']:
            yield scrapy.Request(url, callback=self.parse)
        for local_url in item['local_urls_set']:
            yield scrapy.Request(local_url, callback=self.parse)
