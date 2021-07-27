# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import ShopItem,OfficeItem
import copy
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from scrapy import signals
from pydispatch import dispatcher

class FtxSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def __init__(self):
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting['SELENIUM_TIMEOUT']
        self.isLoadImage = self.mySetting['LOAD_IMAGE']
        self.windowHeight = self.mySetting['WINDOW_HEIGHT']
        self.windowWidth = self.mySetting['windowWidth']
        # 初始化chrome对象
        chrome_opt = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_opt.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_opt)
        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(900, 900)
        self.browser.set_page_load_timeout(self.timeout)  # 页面加载超时时间
        self.browser.set_script_timeout(3)
        self.wait = WebDriverWait(self.browser, 25)  # 指定元素加载超时时间
        super(FtxSpider, self).__init__()
        # 设置信号量，当收到spider_closed信号时，调用mySpiderCloseHandle方法，关闭chrome
        dispatcher.connect(receiver=self.mySpiderCloseHandle,
                           signal=signals.spider_closed
                           )

    # 信号量处理函数：关闭chrome浏览器
    def mySpiderCloseHandle(self, spider):
        print("mySpiderCloseHandle: enter ")
        self.browser.quit()

    def parse(self, response):
        # 提取全国所有城市得url
        trs = response.xpath('//div[@class="outCont"]/table/tr')
        # 省份
        province = None
        # 遍历大陆城市
        for tr in trs[:-2]:
            # 查找所有没有class属性的标签
            tds = tr.xpath('.//td[not(@class)]')
            # 省份
            province_text = tds[0].xpath('.//text()').get()
            # 使用正则将省份中的空白字符替换为空
            province_text = re.sub(r'\s', '', province_text)
            # 如果省份不为空，则将省份保存下来
            if province_text:
                province = province_text
            # 城市信息a标签
            city_links = tds[1].xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('.//text()').get()
                # 城市链接
                city_url = city_link.xpath('.//@href').get()
                newhouse_url = None
                esf_url = None
                shangpu_url = ""
                # 构建写字楼链接
                office_url =""
                if '武汉' in city:
                    # 构建商铺链接
                    sUrl = '/shou/house-a016753/'
                    shangpu_url = city_url.split('.')[0] +'.shop.fang.com'+sUrl
                    # 构建写字楼链接
                    office_url = city_url.split('.')[0] +'.office.fang.com'+sUrl
                    # /zu/house-a016751/  江汉   zu/house-a016753/硚口
                    # 商铺调度请求
                    yield scrapy.Request(url=shangpu_url, callback=self.parser_shangpu, meta={'info': (province, city, shangpu_url,sUrl)})

                # 写字楼调度请求
                # yield scrapy.Request(url=office_url, callback=self.parser_office,  meta={'info': (province, city, office_url,sUrl)})

    # 城市商铺数据
    def parser_shangpu(self, response):
        # 获取省份城市信息
        province, city,shangpu_url,sUrl = response.meta.get('info')

        item = ShopItem(province=province, city=city)
        if('a016753' in sUrl):
                item['district'] = '硚口区'
        elif('a016751' in sUrl):
                item['district'] = '江汉区'
        dls = response.xpath("//div[contains(@class,'shop_list')]/dl")
        for dl in dls:
            name = dl.xpath(".//h4/a[1]/@title").get()
            item['title'] = name
            xiaoqu_address = dl.xpath(".//p[contains(@class,'add_shop')]/a[1]/@title").get()
            item['xiaoqu'] = xiaoqu_address

            address = dl.xpath(".//p[contains(@class,'add_shop')]/span/text()").get()
            item['address'] = address
            U = shangpu_url.replace(sUrl,'')
            newUrl = U + dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
            item['origin_url'] = U + dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
            all_text = ','.join(dl.xpath(".//p[@class='tel_shop']/text()").getall()).strip()\
                .replace('\n', '').replace('\t', '')

            single_text = all_text.split(',')
            if len(single_text) >= 3:
                if len(single_text[2].split(':')) > 1:
                    area = single_text[2].split(':')[1]
                    floor = single_text[1].split('：')[1]
                    type = single_text[0].split('：')[1]
                else:
                    area = single_text[2].split(':')[0]
                    floor = single_text[1].split('：')[0]
                    type = single_text[0].split('：')[0]
            else:
                area = None
                floor = None
            item['floor'] = floor
            item['area'] = area
            item['type'] = type

            price = ''.join(dl.xpath(".//dd[@class='price_right']/span[1]//text()").getall())\
                .replace('\n', '').replace('\t', '')
            item['total_price'] = price
            # 单价
            item['price'] = dl.xpath('.//dd[@class="price_right"]/span[not(@class)]/text()').get()
            meta = {'item': item, 'dont_retry': True}
            yield scrapy.Request(url=newUrl, meta={'item': copy.deepcopy(item)},dont_filter=True,
                                 callback=self.parse_detail_shangpu)
            # yield item

        parrern = re.compile("(house/i3).*(末页)")
        urls = parrern.search(response.text)
        if urls:
            last_num = int(urls.group().split("/")[1].split("i3")[1])
            print(last_num)
            for i in range(2, last_num + 1):
                i = str(i)
                url = "/shou/house/i3" + i + '/'
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse_shangpu,dont_filter=True,
                                     meta={"info": (province, city,shangpu_url,sUrl)})


    # 城市写字楼数据
    def parser_office(self, response):
        # 获取省份城市信息
        province, city, office_url,sUrl = response.meta.get('info')
        # 格式化数据
        item = OfficeItem(province=province, city=city)
        if('a016753' in sUrl):
                item['district'] = '硚口区'
        elif('a016751' in sUrl):
                item['district'] = '江汉区'
        # 每一页所有写字楼信息
        dls = response.xpath('//div[@class="shop_list shop_list_4"]/dl[@dataflag]')
        for dl in dls:
            try:
                # 写字楼标题名
                item['title'] = dl.xpath('.//h4[@class="clearfix"]/a/@title').get()
                detail_url = dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
                # 总价
                item['price'] = dl.xpath('.//dd[@class="price_right"]/span/b/text()').get()
                # 单价
                item['total_price'] = dl.xpath('.//dd[@class="price_right"]/span[not(@class)]/text()').get()
                # tel_shop
                tel_shop_list = dl.xpath('.//p[@class="tel_shop"]/text()').getall()
                # 将住房详情信息中的空白字符去掉
                tel_shop_list = list(map(lambda x: re.sub(r'\s', '', x), tel_shop_list))
                for info in tel_shop_list:
                    if '级' in info:
                        item['dengji'] = info  # 厅室
                    elif '㎡' in info:
                        item['area'] = info  # 面积
                    elif '层' in info:
                        item['floor'] = info  # 楼层
                    elif '向' in info:
                        item['toward'] = info  # 朝向
                    elif '建' in info:
                        item['build'] = info  # 建成年限
                address = dl.xpath(".//p[contains(@class,'add_shop')]/span/text()").get()
                big_address = dl.xpath(".//p[contains(@class,'add_shop')]/a[1]/@title").get()
                # 小区
                item['xiaoqu'] = big_address
                # 地址
                item['address'] = address
                # 交通
                # item['traffic'] = dl.xpath('.//span[@class="bg_none icon_dt"]/text()').get()
                # 详情页链接获取
                U = office_url.replace(sUrl,'')
                newUrl = U + dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
                item['origin_url'] = U + dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
                yield scrapy.Request(url=newUrl, meta={'item': copy.deepcopy(item)},dont_filter=True,
                                      callback=self.parse_detail_office)
                # yield item

            except Exception as e:
                print(e)
        try:
            # 下一页链接
            next_url = response.xpath('//div[@class="page_al"]/p[a="下一页"]/a/@href').get()
            # 将下一页请求交给引擎
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parser_office,dont_filter=True,
                                 meta={'info': (province, city, office_url,sUrl)})
        except Exception as e:
            print(e)


    # 获取商铺详情页信息
    def parse_detail_shangpu(self, response):
        item = response.meta['item']
        dds = response.xpath("/html/body/div[3]/div[4]/div[1]/div[2]/div[2]").css("dd")
        dls = response.xpath("//div[contains(@class,'text-item clearfix')]")
        for dl in dls:
            biaoqian = dl.xpath(".//span[@class='lab']/text()").get()
            content = dl.xpath(".//span[@class='rcont']/text()").get()
            if("挂牌时间" in biaoqian):
                item['guapaishijian'] =content.replace('\n','').replace('\t','').replace(' ','')
            elif("转让费" in biaoqian):
                item['zhuanrangfei'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("物业费" in biaoqian):
                item['wuyefei'] =content.replace('\n','').replace('\t','').replace(' ','')
            elif("楼层" in biaoqian):
                item['floor'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("装修" in biaoqian):
                item['zhuangxiu'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("支付方式" in biaoqian):
                item['zhifufangshi'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("适合经营" in biaoqian):
                item['use_for'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("免租期" in biaoqian):
                item['mianzuqi'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("楼盘名称" in biaoqian):
                item['xiaoqu'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("类型" in biaoqian):
                item['type'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("层高" in biaoqian):
                item['height'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("进深" in biaoqian):
                item['deep'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("面宽" in biaoqian):
                item['weight'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("起租期" in biaoqian):
                item['qizuqi'] = content.replace('\n','').replace('\t','').replace(' ','')
        yield item



    # 获取写字楼详情页信息
    def parse_detail_office(self, response):
        item = response.meta['item']
        # dds = response.xpath("/html/body/div[3]/div[4]/div[1]/div[2]/div[2]").css("dd")
        dls = response.xpath("//div[contains(@class,'text-item clearfix')]")
        for dl in dls:
            biaoqian = dl.xpath(".//span[@class='lab']/text()").get()
            content = dl.xpath(".//span[@class='rcont']/text()").get()
            if("挂牌时间" in biaoqian):
                item['guapaishijian'] =content.replace('\n','').replace('\t','').replace(' ','')
            elif("转让费" in biaoqian):
                item['zhuanrangfei'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("物业费" in biaoqian):
                item['wuyefei'] =content.replace('\n','').replace('\t','').replace(' ','')
            elif("楼层" in biaoqian):
                item['floor'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("装修" in biaoqian):
                item['zhuangxiu'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("支付方式" in biaoqian):
                item['zhifufangshi'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("等级" in biaoqian):
                item['dengji'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("免租期" in biaoqian):
                item['mianzuqi'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("楼盘名称" in biaoqian):
                item['xiaoqu'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("类型" in biaoqian):
                item['type'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("层高" in biaoqian):
                item['height'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("进深" in biaoqian):
                item['deep'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("面宽" in biaoqian):
                item['weight'] = content.replace('\n','').replace('\t','').replace(' ','')
            elif("起租期" in biaoqian):
                item['qizuqi'] = content.replace('\n','').replace('\t','').replace(' ','')
        yield item

