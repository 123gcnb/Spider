import requests
import lxml.html
import time
class spider:
    def __init__(self,page,url_search,header,search_n,colect_mongodb,client_redis,sort,sort_num):
        self.num = 0
        t = 0
        for i in range(0, len(page)):
            start0=time.time()
            url_search_m = url_search + "&keyword=" + search_n + "&wq=" + search_n + sort[sort_num] + "&page=" + page[i]
            # search
            text_quan = requests.get(url_search_m, headers=header).content.decode()
            str_n = lxml.html.fromstring(text_quan)
            str_z = str_n.xpath('//*[@id="J_goodsList"]/ul')
            str_dianpu = str_z[0].xpath('//*[@class="p-shop"]/span/a/@title')
            str_price = str_z[0].xpath('//*[@class="p-price"]/strong/i/text()')
            str_url = str_z[0].xpath('//*[@class="p-name p-name-type-2"]/a/@href')
            for i in range(len(str_dianpu)):
                data = {
                    "id": t,
                    "商品名称": "",
                    "商品价格": float(str_price[i]),
                    "网址": 'https:' + str_url[i],
                    "店铺": str_dianpu[i],
                    "商品信息": ""
                }
                colect_mongodb.insert_one(data)
                t += 1
            self.num += len(str_url)
            for i in range(len(str_url)):
                url_m = 'https:' +str_url[i]
                client_redis.lpush(search_n, url_m)
            time.sleep(0.5)
            end0=time.time()
            if (int(end0 - start0)) % 20 == 0:
                print("。", end="")
        l=0
        start1=time.time()
        while l < self.num:
            url = client_redis.rpop(search_n)
            str = requests.get(url, headers=header).content.decode()
            time.sleep(0.5)
            str_main = lxml.html.fromstring(str)
            str_main1 = str_main.xpath('//*[contains(@class,"itemInfo-wrap")]')
            name = str_main1[0].xpath('//*[@class="sku-name"]')
            name1 = name[0].xpath("string(.)").strip()
            detail = str_main.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li/text()')
            try:
                value = {"id": l}
                shangping = colect_mongodb.find_one(value)
                detail1 = " ".join(detail)
                data1 = {
                         "商品名称": name1,
                        "商品价格": shangping['商品价格'],
                        "网址": shangping['网址'],
                        "店铺": shangping['店铺'],
                        "商品信息": detail1
                }
                colect_mongodb.delete_one(value)
                colect_mongodb.insert_one(data1)
            except:
                print("。",end="")
            l += 1
            end1=time.time()
            if (int(end1-start1))%20==0:
                print("。",end="")
        print("\n")
    def getnum(self):
        return self.num