# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import ZufangItem
import time
from datetime import datetime,timedelta
import datetime as formattime
import re
import random
import platform
import json
import os
import urllib
from urllib.parse import urlparse
import requests
import emoji
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver import ChromeOptions, ActionChains
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# 租房
class ZufangSpider(scrapy.Spider):
    name = 'zufangSpider'
    spiderUrl = 'https://m.anjuke.com/zufang/m/house/api_houselist_data_Jgs?page={}&search_firstpage=1&search_param=%7B%22city_id%22%3A3%2C%22platform%22%3A3%2C%22select_type%22%3A1%2C%22page_size%22%3A30%2C%22cityDomain%22%3A%22gz%22%2C%22cityListName%22%3A%22gz%22%2C%22sid%22%3A%22d0548cba8e891a9978f6c74d3fafb675%22%7D&font_encrypt='
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''
    realtime = False

    headers = {
        "Cookie":"输入自己的cookie"
    }

    def __init__(self,realtime=False,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime=='true'

    def start_requests(self):

        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '9krj0476_zufang') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        pageNum = 1 + 1
        for url in self.start_urls:
            if '{}' in url:
                for page in range(1, pageNum):
                    next_link = url.format(page)
                    yield scrapy.Request(
                        url=next_link,
                        headers=self.headers,
                        callback=self.parse
                    )
            else:
                yield scrapy.Request(
                    url=url,
                    headers=self.headers,
                    callback=self.parse
                )

    # 列表解析
    def parse(self, response):
        _url = urlparse(self.spiderUrl)
        self.protocol = _url.scheme
        self.hostname = _url.netloc
        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '9krj0476_zufang') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        data = json.loads(response.body)
        try:
            list = data["data"]["list"]
        except:
            pass
        for item in list:
            fields = ZufangItem()


            try:
                fields["title"] = str( item["property"]["base"]["title"])

            except:
                pass
            try:
                fields["photo"] = str( item["property"]["base"]["default_photo"])

            except:
                pass
            try:
                fields["postdate"] = str( item["property"]["base"]["post_date"])

            except:
                pass
            try:
                fields["renttype"] = str( item["property"]["base"]["rent_type"])

            except:
                pass
            try:
                fields["price"] = float( item["property"]["base"]["attribute"]["price"])
            except:
                pass
            try:
                fields["areanum"] = float( item["property"]["base"]["attribute"]["area_num"])
            except:
                pass
            try:
                fields["floor"] = int( item["property"]["base"]["attribute"]["floor"])
            except:
                pass
            try:
                fields["geju"] = str( item["property"]["base"]["attribute"]["room_num"]+"室"+item["property"]["base"]["attribute"]["toilet_num"]+"厅")

            except:
                pass
            try:
                fields["address"] = str( item["community"]["base"]["name"])

            except:
                pass
            try:
                fields["laiyuan"] = str("https://gz.zu.anjuke.com/fangyuan/"+str( item["property"]["base"]["house_id"]))

            except:
                pass

            yield fields

    # 详情解析
    def detail_parse(self, response):
        fields = response.meta['fields']
        return fields

    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spider9krj0476?charset=UTF8MB4')
        df = pd.read_sql('select * from zufang limit 50', con = engine)

        # 重复数据过滤
        df.duplicated()
        df.drop_duplicates()

        #空数据过滤
        df.isnull()
        df.dropna()

        # 填充空数据
        df.fillna(value = '暂无')

        # 异常值过滤

        # 滤出 大于800 和 小于 100 的
        a = np.random.randint(0, 1000, size = 200)
        cond = (a<=800) & (a>=100)
        a[cond]

        # 过滤正态分布的异常值
        b = np.random.randn(100000)
        # 3σ过滤异常值，σ即是标准差
        cond = np.abs(b) > 3 * 1
        b[cond]

        # 正态分布数据
        df2 = pd.DataFrame(data = np.random.randn(10000,3))
        # 3σ过滤异常值，σ即是标准差
        cond = (df2 > 3*df2.std()).any(axis = 1)
        # 不满⾜条件的⾏索引
        index = df2[cond].index
        # 根据⾏索引，进⾏数据删除
        df2.drop(labels=index,axis = 0)

    # 去除多余html标签
    def remove_html(self, html):
        if html == None:
            return ''
        pattern = re.compile(r'<[^>]+>', re.S)
        return pattern.sub('', html).strip()

    # 数据库连接
    def db_connect(self):
        type = self.settings.get('TYPE', 'mysql')
        host = self.settings.get('HOST', 'localhost')
        port = int(self.settings.get('PORT', 3306))
        user = self.settings.get('USER', 'root')
        password = self.settings.get('PASSWORD', '123456')

        try:
            database = self.databaseName
        except:
            database = self.settings.get('DATABASE', '')

        if type == 'mysql':
            connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password, charset='utf8')
        else:
            connect = pymssql.connect(host=host, user=user, password=password, database=database)
        return connect

    # 断表是否存在
    def table_exists(self, cursor, table_name):
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]

        if table_name in table_list:
            return 1
        else:
            return 0

    # 数据缓存源
    def temp_data(self):

        connect = self.db_connect()
        cursor = connect.cursor()
        sql = '''
            insert into `zufang`(
                id
                ,title
                ,photo
                ,postdate
                ,renttype
                ,price
                ,areanum
                ,floor
                ,geju
                ,address
                ,laiyuan
            )
            select
                id
                ,title
                ,photo
                ,postdate
                ,renttype
                ,price
                ,areanum
                ,floor
                ,geju
                ,address
                ,laiyuan
            from `9krj0476_zufang`
            where(not exists (select
                id
                ,title
                ,photo
                ,postdate
                ,renttype
                ,price
                ,areanum
                ,floor
                ,geju
                ,address
                ,laiyuan
            from `zufang` where
                `zufang`.id=`9krj0476_zufang`.id
            ))
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
