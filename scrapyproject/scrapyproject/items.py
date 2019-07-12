# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem 

# class ScrapyprojectItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

import sys
print('@'*50)
print(sys.path)


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'pricetracker.settings'

from track.models import Product
class ScrapyprojectItem(DjangoItem):
        print('1'*50)
        django_model = Product