# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class DataworkPipeline(object):
    def process_item(self, item, spider):
        return item


class PageItemPipeline(object):
    def process_item(self, item, spider):
        with open('test.txt', 'ab') as fp:

            fp.write(item['url'].encode('utf8') + b'\n')
            fp.write(item['title'].encode('utf8') + b'\n')
            fp.write(item['keywords'].encode('utf8') + b'\n')
            fp.write(item['description'].encode('utf8') + b'\n')
            for local_url in item['local_urls_set']:
                fp.write(local_url.encode('utf8') + b'\n')
            for external_url in item['external_urls_set']:
                fp.write(external_url.encode('utf8') + b'\n')
