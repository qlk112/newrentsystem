# 数据容器文件

import scrapy

class SpiderItem(scrapy.Item):
    pass

class ZufangItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 图片
    photo = scrapy.Field()
    # 更新时间
    postdate = scrapy.Field()
    # 类型
    renttype = scrapy.Field()
    # 价格（元/月）
    price = scrapy.Field()
    # 面积（平米）
    areanum = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 格局
    geju = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 来源
    laiyuan = scrapy.Field()

