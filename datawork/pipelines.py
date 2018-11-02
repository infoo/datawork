# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
from datawork.other.sqltool import getConnection, SqlTool
from datawork.other.segtool import SegTool
import threading


class DataworkPipeline(object):
    def process_item(self, item, spider):
        return item


class PageItemPipeline(object):
    sql_tool = SqlTool(getConnection())

    def __init__(self):
        self.db = PageItemPipeline.sql_tool

    # 默认执行的方法
    def process_item(self, item, spider):
        self.process_content(item)
        self.insert_item_toMySQL(item)

    # 写到数据库
    def insert_item_toMySQL(self, item):
        st_url_id = -1
        url = item['url']
        item_url = self.db.select_url(url)
        if item_url is None:
            # 如果该url 不在数据库则插入
            st_url_id = self.db.insert_url(url)
        else:
            st_url_id = item_url[0]
        for u in item['local_urls_set']:
            # 遍历该页面的出链接
            res = self.db.select_url(u)
            if res is None:
                # 如果该url 不在数据库则插入
                ed_url_id = self.db.insert_url(u)
                # 同时插入该关系
                self.db.insert_url_out(st_url_id, ed_url_id)
            else:
                ed_url_id = res[0]
                # 同时插入该关系
                self.db.insert_url_out(st_url_id, ed_url_id)

        for u in item['external_urls_set']:
            # 遍历该页面的出链接
            res = self.db.select_url(u)
            if res is None:
                # 如果该url 不在数据库则插入
                ed_url_id = self.db.insert_url(u)
                # 同时插入该关系
                self.db.insert_url_out(st_url_id, ed_url_id)
            else:
                ed_url_id = res[0]
                # 同时插入该关系
                self.db.insert_url_out(st_url_id, ed_url_id)

        content = item['content']
        self.db.insert_page(st_url_id, content)

    # 写到硬盘
    def write_item_toDisk(self, item):
        fileDir = 'd:/res/' + item['host']
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
        filepath = fileDir + '/' + item['file']
        with open(filepath, 'ab') as fp:
            fp.write(item['url'].encode('utf8') + b'\n')
            fp.write(item['title'].encode('utf8') + b'\n')
            fp.write(item['keywords'].encode('utf8') + b'\n')
            fp.write(item['description'].encode('utf8') + b'\n')
            fp.write(item['content'].encode('utf8') + b'\n')
            for local_url in item['local_urls_set']:
                fp.write(local_url.encode('utf8') + b'\n')
            for external_url in item['external_urls_set']:
                fp.write(external_url.encode('utf8') + b'\n')

    ##处理content
    def process_content(self, item):
        body = item['content']
        # 删除脚本
        script = re.compile('(<script[\s\S]*?</script>)|(<style[\s\S]*?</style>)')
        body = script.sub('', body)
        # 删除全部标签 <>
        tag = re.compile('(</?[^<>]*>)|(<!--[\s\S]*?-->)|(//.*\s*?\n)')
        body = tag.sub('', body)
        # 过滤换行,将多次换行改为1次换行
        sp = re.compile('[\s]+')  # 大于等于1次换行
        body = sp.sub(' ', body)
        # 去掉非汉字 非字母 以及 非换行 和 非小数点
        other = re.compile('[^\u2E80-\u9FFF\w\n\.]')
        item['content'] = other.sub('', body)
        th = threading.Thread(target=self.process_content_jieba_cut, args=(body,))
        th.start()

    def process_content_jieba_cut(self, body):
        SegTool.cut_and_insert_to_seg(body)
