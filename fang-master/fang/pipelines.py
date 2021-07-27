# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class FangPipeline(object):
    def process_item(self, item, spider):
        return item


class HousePipeline(object):
    def open_spider(self, spider):
        if spider.name == "shangpu":
            self.file = open('shangpu.txt', 'w', encoding="utf-8")
        elif spider.name == "ftx":
            self.file = open('ftx.txt', 'w', encoding="utf-8")
        else:
            self.file = open(spider.name + '.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        content = dict(item)

        content = json.dumps(content, ensure_ascii=False)
        self.file.write(content + "\n")
        return item

    # 出错处理
    def handle_error(self, error, item, spider):
        print(error)


