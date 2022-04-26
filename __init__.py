import time
from mian.connectdb import connectdb
from mian.printall import printall
from mian.shuru import shuru
from mian.spider import spider

if __name__=="__main__":
    header={ # 啊沙发沙发
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'cookie':""#cookie of　https://www.jd.com/
    }
    start=time.time()
    #如下三行为cookie输入，如果已经在header中添加COOKIE可在下列三行开头加上#，以注释下列三行
    print("Please enter cookie of　https://www.jd.com/")
    cookie=input()
    header['cookie']=cookie
    print("Please enter what you want to inquire about")
    search_n = input()
    shuru = shuru(search_n=search_n)
    url_search = shuru.geturl()
    dir = shuru.getdir()
    connect = connectdb(search_n=search_n)
    client_redis = connect.get_client_redis()
    colect_mongodb = connect.get_colect_mongodb()
    sort_pin = ["价格升序", "价格降序", "销量", "评论量"]
    # psort=1--价格升序
    # psort=2--价格降序
    # psort=3--销量
    # psort=4--评论量
    sort = ['&psort=1', '&psort=2', '&psort=3', '&psort=4']
    # 搜索排序方式
    page = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    print("0--价格升序" + "\n"
                      "1--价格降序" + "\n"
                                  "2--销量" + "\n"
                                            "3--评论量")
    print("请输入排序方式")
    sort_num = int(input())
    spider = spider(page=page, url_search=url_search, header=header, search_n=search_n, colect_mongodb=colect_mongodb,
                    client_redis=client_redis, sort_num=sort_num, sort=sort)
    num = spider.getnum()
    printall = printall(dir=dir, colect_mongodb=colect_mongodb, num=num, sort_num=sort_num, sort_pin=sort_pin)
    end = time.time()
    #print(end - start)
