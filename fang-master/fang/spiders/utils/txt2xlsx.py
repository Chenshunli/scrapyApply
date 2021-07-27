import pandas as pd
import xlsxwriter
import json
import re
# from resolve.analyse import simicos
from jieba import posseg

# 原始房价数据
original= 'C:\\Users\\12772\\Desktop\\新建文件夹\\shop_shou_qiaokou2.txt'

# 保存成xls的数据
xlsx_ftx = 'C:\\Users\\12772\\Desktop\\新建文件夹\\shop_shou_qiaokou2.xlsx'

# ===================

# 合并链家安居客，保留2字段数据
merge_ajk_lj_2 = 'merge_ajk_lj_2-12.xlsx'
# 合并链家安居客，保留1字段
merge_ajk_lj_1 = 'merge_ajk_lj_1-12.xlsx'


# 和客户提供的数据做匹配
match_input = 'match_input_xiaoqu.csv'
match_output = 'match_result-6.csv'


def save_xls(filename, headings, result):
    workbook = xlsxwriter.Workbook(filename=filename)
    worksheet = workbook.add_worksheet()
    worksheet.write_row('A1', headings)
    row = 2
    for item in result:
        worksheet.write_row('A{}'.format(row), item)
        row += 1
    workbook.close()


def xiezilou():
    pattern = re.compile('\\d+')

    result = []
    headings = ['province','city','district','title','xiaoqu','address','floor','area', 'type','total_price','price','origin_url','wuyefei','zhuangxiu','zhifufangshi','dengji','weight','deep','height','guapaishijian','xiaoquName', 'lng', 'lat']

    with open(original, 'r', encoding='utf-8') as f1:
        lines = f1.readlines()
        for line in lines:
            data = json.loads(line)
            # if data['district'] == '沌口开发区':
            #     data['district'] = '沌口'
            for head in headings:
                if head not in list(data.keys()):
                    data[head] = ''
            info = [
                data['province'], data['city'],data['district'], data['title'], data['xiaoqu'], data['address'],data['floor'],data['area'],  data['type'], data['total_price'],data['price'],
                data['origin_url'],data['wuyefei'],data['zhuangxiu'],data['zhifufangshi'],data['dengji'],data['weight'],data['deep'],data['height'],data['guapaishijian'],data['xiaoquName'],data['lng'],data['lat'],
            ]
            result.append(info)

    save_xls(filename=xlsx_ftx, headings=headings, result=result)



def shop():
    pattern = re.compile('\\d+')

    result = []
    headings = ['province','city','district','title','xiaoqu','address','floor','area', 'type','total_price','price','origin_url','zhuanrangfei','wuyefei','zhuangxiu','zhifufangshi','use_for','weight','deep','height','guapaishijian','xiaoquName', 'lng', 'lat']

    with open(original, 'r', encoding='utf-8') as f1:
        lines = f1.readlines()
        for line in lines:
            data = json.loads(line)
            # if data['district'] == '沌口开发区':
            #     data['district'] = '沌口'
            for head in headings:
                if head not in list(data.keys()):
                    data[head] = ''
            info = [
                data['province'], data['city'],data['district'], data['title'], data['xiaoqu'], data['address'],data['floor'],data['area'],  data['type'], data['total_price'],data['price'],
                data['origin_url'],data['zhuanrangfei'],data['wuyefei'],data['zhuangxiu'],data['zhifufangshi'],data['use_for'],data['weight'],data['deep'],data['height'],data['guapaishijian'],data['xiaoquName'],data['lng'],data['lat'],
            ]
            result.append(info)

    save_xls(filename=xlsx_ftx, headings=headings, result=result)


def anjuke():
    result = []
    headings = ['district', 'area', 'name', 'price', 'wuye_type', 'wuye_fee', 'buildup_area', 'rooms', 'build_date',
                'parking',
                'plot_ratio', 'afforestation_rate', 'dev', 'wuye', 'detail_xiaoqu_name', 'lng', 'lat']
    int_pattern = re.compile('\\d+')
    point_pattern = re.compile('\\d+.?\\d+%?')

    with open(original_ajk, 'r', encoding='utf-8') as f1:
        for line in f1:
            data = json.loads(line)
            for head in headings:
                if head not in list(data.keys()):
                    data[head] = ''
            searchObj = point_pattern.search(data['wuye_fee'])
            try:
                if searchObj:
                    wuye_fee = searchObj.group(0)
                else:
                    wuye_fee = ''
                data['wuye_fee'] = wuye_fee
                searchObj = int_pattern.search(data['buildup_area'])
                if searchObj:
                    buildup_area = searchObj.group(0)
                else:
                    buildup_area = ''
                data['buildup_area'] = buildup_area
                searchObj = int_pattern.search(data['rooms'])
                if searchObj:
                    rooms = searchObj.group(0)
                else:
                    rooms = ''
                data['rooms'] = rooms
                searchObj = int_pattern.search(data['build_date'])
                if searchObj:
                    build_date = searchObj.group(0)
                else:
                    build_date = ''
                data['build_date'] = build_date
                searchObj = point_pattern.search(data['afforestation_rate'])
                if searchObj:
                    afforestation_rate = searchObj.group(0)
                else:
                    afforestation_rate = ''
                data['afforestation_rate'] = afforestation_rate
            except Exception:
                print(data)
            headings = ['district', 'area', 'name', 'price', 'wuye_type', 'wuye_fee', 'buildup_area', 'rooms',
                        'build_date',
                        'parking',
                        'plot_ratio', 'afforestation_rate', 'dev', 'wuye', 'detail_xiaoqu_name', 'lng', 'lat']
            info = [
                data['district'], data['area'], data['name'], data['price'], data['wuye_type'], data['wuye_fee'],
                data['buildup_area'],
                data['rooms'], data['build_date'], data['parking'], data['plot_ratio'], data['afforestation_rate'],
                data['dev'], data['wuye'], data['detail_xiaoqu_name'],
                data['lng'], data['lat'],
            ]
            result.append(info)

    save_xls(filename=xlsx_ajk, headings=headings, result=result)


# 合并链家安居客，保留两个字段
def merge():
    # 链家
    # district	area	name	price	on_sale	build_date	build_type	wuye
    # dev	buildings	rooms	detail_xiaoqu_name	lng	lat	经度	纬度

    # 安居客
    # district	area	name	price	wuye_type	wuye_fee	buildup_area
    # rooms	build_date	parking	plot_ratio	afforestation_rate	dev	wuye
    # detail_xiaoqu_name	lng	lat	经度(转换后)	纬度(转换后)
    headings = [
        'district1', 'district2', 'area1', 'area2', 'name1', 'name2', 'price1', 'price2', 'on_sale', 'build_date1',
        'build_date2',
        'build_type', 'wuye1', 'wuye2', 'dev1', 'dev2', 'buildings', 'rooms1', 'rooms2', 'detail_xiaoqu_name',
        'lng1', 'lat1', 'lng2', 'lat2', 'wuye_type', 'wuye_fee', 'buildup_area', 'parking', 'plot_ratio',
        'afforestation_rate'
    ]
    results = []
    ajk_data = pd.read_excel(xlsx_ajk, encoding='gbk')
    lj_data = pd.read_excel(xlsx_lj, encoding='gbk')
    ajk_json = json.loads(ajk_data.to_json(orient='records', force_ascii=False))
    lj_json = json.loads(lj_data.to_json(orient='records', force_ascii=False))
    lj_index = []
    ajk_index = []
    for j, ajk in enumerate(ajk_json):
        for i in range(len(lj_json)):
            if ajk['district'] == lj_json[i]['district'] and \
                    (ajk['name'] in lj_json[i]['name'] or lj_json[i]['name'] in ajk['name']):
                data = [
                    lj_json[i]['district'], ajk['district'], lj_json[i]['area'], ajk['area'], lj_json[i]['name'],
                    ajk['name'],
                    lj_json[i]['price'],
                    ajk['price'], lj_json[i]['on_sale'], lj_json[i]['build_date'], ajk['build_date'],
                    lj_json[i]['build_type'], lj_json[i]['wuye'], ajk['wuye'], lj_json[i]['dev'],
                    ajk['dev'], lj_json[i]['buildings'], lj_json[i]['rooms'], ajk['rooms'],
                    lj_json[i]['detail_xiaoqu_name'], lj_json[i]['lng'], lj_json[i]['lat'], ajk['lng'],
                    ajk['lat'], ajk['wuye_type'], ajk['wuye_fee'], ajk['buildup_area'], ajk['parking'],
                    ajk['plot_ratio'], ajk['afforestation_rate']
                ]
                lj_index.append(i)
                ajk_index.append(j)
                results.append(data)
                break

    for i, ajk in enumerate(ajk_json):
        if i in ajk_index:
            continue
        data = [
            '', ajk['district'], '', ajk['area'], '', ajk['name'], '', ajk['price'], '', '', ajk['build_date'], '', '',
            ajk['wuye'], '', ajk['dev'], '', '', ajk['rooms'], ajk['detail_xiaoqu_name'], '', '', ajk['lng'],
            ajk['lat'], ajk['wuye_type'],
            ajk['wuye_fee'], ajk['buildup_area'], ajk['parking'], ajk['plot_ratio'], ajk['afforestation_rate']
        ]
        results.append(data)
    for i in range(len(lj_json)):
        if i in lj_index:
            continue
        data = [
            lj_json[i]['district'], '', lj_json[i]['area'], '', lj_json[i]['name'], '', lj_json[i]['price'], '',
            lj_json[i]['on_sale'], lj_json[i]['build_date'], '',
            lj_json[i]['build_type'],
            lj_json[i]['wuye'], '', lj_json[i]['dev'], '', lj_json[i]['buildings'], lj_json[i]['rooms'], '',
            lj_json[i]['detail_xiaoqu_name'],
            lj_json[i]['lng'], lj_json[i]['lat'], '', '', '', '', '', '', '', ''
        ]
        results.append(data)
    save_xls(merge_ajk_lj_2, headings, results)


# 基于合并后的链家安居客的两个字段，保留一个字段
def merge2():
    headings = [
        'district', 'area', 'name', 'price', 'on_sale', 'build_date',
        'build_type', 'wuye_type', 'wuye', 'dev', 'buildings', 'rooms', 'detail_xiaoqu_name',
        'lng', 'lat', 'wuye_fee', 'buildup_area', 'parking', 'plot_ratio', 'afforestation_rate'
    ]
    data = pd.read_excel(merge_ajk_lj_2, encoding='gbk')
    datas = json.loads(data.to_json(orient='records', force_ascii=False))
    result = []
    none_data = ['暂无数据', '无', '', None]
    for item in datas:
        price = item['price1'] if item['price2'] in none_data else item['price2']
        wuye = item['wuye1'] if item['wuye2'] in none_data else item['wuye2']
        dev = item['dev1'] if item['dev2'] in none_data else item['dev2']
        build_date = item['build_date1'] if item['build_date2'] in none_data else item['build_date2']
        # rooms = item['rooms1'] if item['rooms2'] in none_data else item['rooms2']
        if item['rooms1'] is not None and item['rooms2'] is not None:
            rooms = max(item['rooms1'], item['rooms2'])
        else:
            rooms = item['rooms1'] if item['rooms2'] in none_data else item['rooms2']
        buildings = item['buildings']
        if buildings is not None and rooms is not None:
            if int(buildings) > int(rooms):
                print(item)
                continue
        district = item['district1'] if item['district2'] in none_data else item['district2']
        area = item['area1'] if item['area2'] in none_data else item['area2']
        name = item['name1'] if item['name2'] in none_data else item['name2']
        lng = item['lng1'] if item['lng2'] in none_data else item['lng2']
        lat = item['lat1'] if item['lat2'] in none_data else item['lat2']
        iiitem = [
            district, area, name, price,
            item['on_sale'], build_date,
            item['build_type'], item['wuye_type'], wuye, dev, item['buildings'], rooms,
            item['detail_xiaoqu_name'], lng, lat, item['wuye_fee'], item['buildup_area'], item['parking'],
            item['plot_ratio'], item['afforestation_rate']
        ]
        result.append(iiitem)
    save_xls(merge_ajk_lj_1, headings, result)


# 和客户提供的数据和处理后加入街道信息的房价做匹配
def match_for_gtj():
    import copy

    headings = [
        'OBJECTID', 'NAME', 'XIAOQUNUM', 'SSQ', 'SSJ', 'SSSQ', 'SQBM',
        'fj_OBJECTID_1', 'fj_OBJECTID', 'district', 'area', 'name', 'price', 'on_sale', 'build_date',
        'build_type', 'wuye_type', 'wuye', 'dev', 'buildings', 'rooms', 'detail_xia',
        'lng', 'lat', 'wuye_fee', 'buildup_ar', 'parking', 'plot_ratio', 'afforestat',
        'id', 'FID_1', 'fj_OBJECTID_2', 'fj_SSQ', 'QBM', 'fj_SSJ', 'JBM', 'fj_SSSQ', 'fj_SQBM', 'WGLB', 'similarity'
    ]
    xq = pd.read_csv(match_input, encoding='gbk')
    xq_datas = json.loads(xq.to_json(orient='records', force_ascii=False))
    excludes = ['小学', '中学', '医院', '中心', '酒店', '学校', '敬老院', '大学', '办事处', '街道办', '广场', '村', '门诊部',
                '药房', '旧址']
    xq_datass = []
    for xq_data in xq_datas:
        ffflag = 0
        for exclude_key in excludes:
            # 过滤
            if xq_data['NAME'] is None or exclude_key in xq_data['NAME']:
                ffflag = 1
                break
        if ffflag == 0:
            xq_datass.append(xq_data)

    xq_datas = xq_datass

    fj = pd.read_excel('fj.xlsx', encoding='gbk')
    fj_datas = json.loads(fj.to_json(orient='records', force_ascii=False))
    results = []
    count = 0
    for xq_data in xq_datas:
        confs = []
        result = [xq_data[k] for k in xq_data.keys()]
        for fj_data in fj_datas:
            if xq_data['NAME'] is None:
                continue
            # if xq_data['SSQ'] == fj_data['SSQ'] and xq_data['SSJ'] == fj_data['SSJ'] and \
            #         xq_data['SSSQ'] == fj_data['SSSQ'] and (
            #         xq_data['NAME'] in fj_data['name'] or fj_data['name'] in xq_data['NAME']):
            if xq_data['SSQ'] == fj_data['SSQ'] and xq_data['SSJ'] == fj_data['SSJ'] and \
                    xq_data['SSSQ'] == fj_data['SSSQ'] and simicos(fj_data['name'], xq_data['NAME']) >= 0.1:
                temp = copy.deepcopy(result)
                for k in fj_data.keys():
                    temp.append(fj_data[k])
                temp.append(simicos(fj_data['name'], xq_data['NAME']))
                confs.append(temp)
        if len(confs) == 1:
            results.append(confs[0])
        elif len(confs) > 1:
            max_conf = max(confs, key=lambda x: x[len(x) - 1])
            results.append(max_conf)
        else:
            count += 1
            for i in range(len(fj_datas[0])):
                result.append(' ')
            result.append(0)
            results.append(result)
    print('未匹配成功', count)
    save_xls('xqmfj_similarity_0.1.xlsx', headings, results)


def save_cut_words():
    headings = [
        'words'
    ]
    xq = pd.read_csv('data/xq.csv', encoding='gbk')
    xq_datas = json.loads(xq.to_json(orient='records', force_ascii=False))
    excludes = ['小学', '中学', '医院', '中心', '酒店', '学校', '敬老院', '大学', '办事处', '街道办', '广场', '村', '门诊部', '药房']

    xq_datass = []
    for xq_data in xq_datas:
        ffflag = 0
        for exclude_key in excludes:
            if xq_data['NAME'] is None:
                ffflag = 1
                break
            if exclude_key in xq_data['NAME']:
                ffflag = 1
                break
        if ffflag == 0:
            xq_datass.append(xq_data)

    fj = pd.read_excel('fj.xlsx', encoding='gbk')
    fj_datas = json.loads(fj.to_json(orient='records', force_ascii=False))

    flags = ['x']

    results_fj = []
    for fj_data in fj_datas:
        for fj, flag in posseg.lcut(fj_data['name']):
            if flag not in flags:
                results_fj.append([fj, flag])

    save_xls('cut_words_fj.xlsx', headings, results_fj)
    results_fj = []
    for xq_data in xq_datass:
        for xq, flag in posseg.lcut(xq_data['NAME']):
            if flag not in flags:
                results_fj.append([xq, flag])
    save_xls('cut_words_xq.xlsx', headings, results_fj)


# lianjia()
# anjuke()
# fangtianxia()
# 链家安居客字段拼接
# merge()
# 链家安居客字段合并
# merge2()


# 匹配区，街道
if __name__ == '__main__':
    xiezilou()
    # anjuke()
    # shop()
    # merge()
    # merge2()
