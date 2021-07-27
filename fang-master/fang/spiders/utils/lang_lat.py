import json
import requests
import pandas as pd
import openpyxl


class LangAndLat:
    num_count = 0

    def write_name(self, src_file, dist_file,district):
        with open(src_file, "r", encoding="utf-8") as f1, \
                open(dist_file, "w", encoding="utf-8") as f2:
            for line in f1:
                line_dict = json.loads(line)
                if district == '江汉区':
                    line_dict['xiaoquName'] = "武汉市江汉区" + line_dict['address']+line_dict['xiaoqu']
                else:
                    line_dict['xiaoquName'] = "武汉市硚口区" + line_dict['address'] + line_dict['xiaoqu']
                line_dict.update(self.baidu_api(line_dict['xiaoquName']))
                f2.write(json.dumps(line_dict, ensure_ascii=False) + "\n")

    # 商铺文件获取坐标
    def write_name2(self, src_file, dist_file,district):
        with open(src_file, "r", encoding="utf-8") as f1, \
                open(dist_file, "w", encoding="utf-8") as f2:
            for line in f1:
                line_dict = json.loads(line)
                if district == '江汉区':
                    line_dict['xiaoquName'] = "武汉市江汉区" + line_dict['address']+line_dict['xiaoqu']
                else:
                    line_dict['xiaoquName'] = "武汉市硚口区" + line_dict['address'] + line_dict['xiaoqu']
                line_dict.update(self.baidu_api(line_dict['xiaoquName']))
                f2.write(json.dumps(line_dict, ensure_ascii=False) + "\n")

    def baidu_api(self, detail_xiaoqu_name):
        base_url = "http://api.map.baidu.com/geocoding/v3/"
        address = detail_xiaoqu_name
        ak1 = "H3LhFUmdqu0eixdO71IXn09xUk3aD1IO"
        ak2 = "mnn9YGdzTpTG81g1cH8Fvgg6COh3Sn2n"
        ak3 = "x7GGRkrhR5YnRBgrwGDnzP5aSpSwRk5s"
        output = "json"
        city = "武汉市"
        self.num_count += 1
        if self.num_count <= 6000:
            ak = ak1
        elif self.num_count <= 12000:
            ak = ak2
        else:
            ak = ak3
        baidu_url = base_url + "?" + "address=" + address + "&ak=" + ak + "&output=" + output + "&city=" + city
        response = requests.get(baidu_url)
        dic = json.loads(response.content, encoding="utf-8")
        print(dic)
        res = dict()
        if dic['status'] == 0:
            res['lng'] = dic['result']['location']['lng']
            res['lat'] = dic['result']['location']['lat']
            res['precise'] = dic['result']['precise']
            res['confidence'] = dic['result']['confidence']
            res['comprehension'] = dic['result']['comprehension']
        else:
            print(detail_xiaoqu_name, dic)
            res['lng'] = ""
            res['lat'] = ""
        # res['precise'] = dic['result']['precise']
        # res['confidence'] = dic['result']['confidence']
        # res['comprehension'] = dic['result']['comprehension']
        # res['level'] = dic['result']['level']
        return res

    def company(self):
        src_data = pd.read_excel('nocompare.xls', encoding='gbk')
        src_datas = json.loads(src_data.to_json(orient='records', force_ascii=False))
        headings = list(src_datas[0].keys())
        headings.extend(['lng', 'lat', 'precise', 'confidence', 'comprehension'])
        results = []
        for src_data in src_datas:
            # name = '武汉市' + src_data['distract'] + src_data['name']
            name = src_data['企业地址']
            if name == '东湖新技术开发区左岭镇左岭路117号光电子配套产业园一期厂房1号楼二层263室(自贸区武汉片区)':
                name = '武汉蔚能电池资产有限公司'
            elif name == '蔡甸区奓山街常福新城启动区湖北总部基地CBD一期二组团项目3栋3层24-29号':
                name = '湖北益丰医药有限公司'
            src_data.update(self.baidu_api(name))
            print(src_data)
            results.append(list(src_data.values()))
        self.append_xls(results, headings, 'qiye_position.xls')

    def append_xls(self, results, headings, file_name='default.xlsx'):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.append(headings)
        for result in results:
            worksheet.append(result)
        workbook.save(file_name)

    def zuobiaoshiqu(self, name):
        url = 'https://api.map.baidu.com/?qt=s&c=218&wd={}&rn=10&ie=utf-8&oue=1&' \
              'fromproduct=jsapi&res=api&callback=BMap._rd._cbk43769&ak=E4805d16520de693a3fe707cdc962045'.format(name)
        json_str = requests.get(url).text.replace("/**/BMap._rd._cbk43769 && BMap._rd._cbk43769", "")[1:-1]
        json_str = json.loads(json_str)
        addr = None
        if json_str.get('content'):
            content = json_str['content'][0]
            if content.get('addr'):
                addr = content['addr']
        return addr

    def check_points(self):
        df = pd.read_excel('qiye2_position.xlsx')
        data_json = json.loads(df.to_json(orient='records', force_ascii=False))
        # data_json = list(filter(lambda x: x['comprehension'] < 100, data_json))
        headings = list(data_json[0].keys())
        results = []
        for data in data_json:
            if data['comprehension'] < 100:
                print("old version ---->", data)
                addr = self.zuobiaoshiqu(data['name'])
                if addr is not None:
                    new_res = self.baidu_api(addr)
                    data.update(new_res)
                    print("new version ---->", data)
            results.append(list(data.values()))

        self.append_xls(results, headings, 'check_qiye2_position.xlsx')

    def save_addr(self):
        df = pd.read_excel('qiye2.xlsx')
        data_json = json.loads(df.to_json(orient='records', force_ascii=False))
        headings = list(data_json[0].keys())
        results = []
        for data in data_json:
            addr = self.zuobiaoshiqu(data['name'])
            addr = '' if addr is None else addr
            data['addr'] = addr
            print(data)
            results.append(list(data.values()))
        self.append_xls(results, headings, 'qiye2_addr.xlsx')

    def save_match_result(self):
        df = pd.read_excel('target2.xls')
        data_json = json.loads(df.to_json(orient='records', force_ascii=False))
        headings = list(data_json[0].keys())
        headings.extend(['lng', 'lat'])
        results = []
        for data in data_json:
            if data['所在行政区'] is not None:
                addr = data['所在行政区'] + data['重点发展区域']
            else:
                addr = data['重点发展区域']
            res = self.baidu_api(addr)
            data.update(res)
            print(data)
            results.append(list(data.values()))
        self.append_xls(results, headings, 'target2_lat_lng.xlsx')


if __name__ == '__main__':
    lang = LangAndLat()
    str = input("请输入类型：")
    str2 = input("请输入区域：")
    if(str=="商铺"):
        if(str2=="硚口"):
            lang.write_name2("C:\\Users\\12772\\Desktop\\新建文件夹\\shop_shou_qiaokou.txt", "C:\\Users\\12772\\Desktop\\新建文件夹\\shop_shou_qiaokou2.txt","硚口区")
        elif(str2=="江汉"):
            lang.write_name2("C:\\Users\\12772\\Desktop\\新建文件夹\\shop_shou_jianghan.txt", "C:\\Users\\12772\\Desktop\\新建文件夹\\shop_shou_jianghan2.txt","江汉区")

    elif(str=="写字楼"):
        if(str2=="硚口"):
            lang.write_name("C:\\Users\\12772\\Desktop\\新建文件夹\\office_shou_qiaokou.txt", "C:\\Users\\12772\\Desktop\\新建文件夹\\office_shou_qiaokou2.txt","硚口区")
        elif(str2=="江汉"):
            lang.write_name("C:\\Users\\12772\\Desktop\\新建文件夹\\office_shou_jianghan.txt", "C:\\Users\\12772\\Desktop\\新建文件夹\\office_shou_jianghan2.txt","江汉区")

    # lang.save_match_result()
    # lang.company()
