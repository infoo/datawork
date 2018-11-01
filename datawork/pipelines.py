# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re


class DataworkPipeline(object):
    def process_item(self, item, spider):
        return item


class PageItemPipeline(object):
    def process_item(self, item, spider):
        body = item['content']
        # 删除脚本
        script = re.compile('<script[\s\S]*</script>')
        body = script.sub('', body)
        # 删除全部标签 <>
        tag = re.compile('(<[^<>]*>)|(<!--[\s\S]*?-->)|(//.*\s*?\n)')
        body = tag.sub('', body)
        # 过滤换行,将多次换行改为1次换行
        sp = re.compile('[\s]{2,}')  # 大于等于1次换行
        body = sp.sub('\n', body)
        # 去掉非汉字 非字母 以及 非换行 和 非小数点
        other = re.compile('[^\u2E80-\u9FFF\w\n\.]')
        body = other.sub('', body)
        fileDir = 'd:/res/'+item['host']
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)

        filepath = fileDir+'/'+item['file']
        with open(filepath, 'ab') as fp:
            fp.write(item['url'].encode('utf8') + b'\n')
            fp.write(item['title'].encode('utf8') + b'\n')
            fp.write(item['keywords'].encode('utf8') + b'\n')
            fp.write(item['description'].encode('utf8') + b'\n')
            fp.write(body.encode('utf8') + b'\n')
            for local_url in item['local_urls_set']:
                fp.write(local_url.encode('utf8') + b'\n')
            for external_url in item['external_urls_set']:
                fp.write(external_url.encode('utf8') + b'\n')
