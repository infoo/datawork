import scrapy
from datawork.items import PageItem
from urllib3.util import Url, parse_url
import re


class PageSpider(scrapy.Spider):
    name = "pageSpider"
    allowed_domains = ['financeun.com']

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
        content = response.xpath('//body').extract()
        item = PageItem()
        item['url'] = response.url
        item['local_urls_set'] = set()
        item['external_urls_set'] = set()
        if len(title) >= 1:
            item['title'] = title[0]
        if len(keywords) >= 1:
            item['keywords'] = keywords[0]
        if len(description) >= 1:
            item['description'] = description[0]
        if len(content) >= 1:
            item['content'] = content[0]
        for href in all_hrefs:
            if href.startswith('/'):
                url = parse_url(response.url + href[1:])
                item['local_urls_set'].add(url.url)
                item['host'] = url.host
                item['file'] = '_'.join(url.path.split('/')[1:])+'.txt'
            if href.startswith('http'):
                item['external_urls_set'].add(href)
        return item
