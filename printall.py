import csv
import matplotlib.pylab as plt
import matplotlib as mpl
import re
class printall:
    def __init__(self,dir,colect_mongodb,sort_pin,sort_num,num):
        #画柱状图
        mpl.rcParams['font.sans-serif'] = ['STZhongsong']  # 指定默认字体：解决plot不能显示中文问题
        mpl.rcParams['axes.unicode_minus'] = False
        def draw(labels, quants):
            plt.subplots(figsize=(16, 9))
            plt.barh(range(len(quants)), quants, tick_label=labels, color="g")
            plt.title("产品" + sort_pin[sort_num] + "TOP 10")
            for y, x in enumerate(quants):
                plt.text(x, y, "%s" % x)
            plt.grid(True)
            plt.savefig(dir + "—TOP 10.png")
            plt.show()
            plt.close()

        labels = []
        quants = []
        labels_text = []
        quants_text = []
        data = colect_mongodb.find({}, {'_id': 0, "商品名称": 1, "商品价格": 1, "网址": 1, "店铺": 1, "商品信息": 1})
        for i in range(10):
            name0 = data[i].get('商品信息')
            name1 = re.findall('商品名称：(.*?)商品', name0)
            name = "".join(name1[0].split())
            price = data[i].get('商品价格')
            labels_text.append(name)
            quants_text.append(price)
        t = 9
        for i in range(10):
            labels.append(labels_text[t])
            quants.append(quants_text[t])
            t -= 1
        draw(labels, quants)
        #画扇形图
        xinxi = []
        shulian = {}
        #data = colect_mongodb.find({}, {'_id': 0, "商品名称": 1, "商品价格": 1, "网址": 1, "店铺": 1, "商品信息": 1})
        for i in range(num - 20):
            dianpu0 = data[i].get('店铺')
            dianpu = "".join(dianpu0.split())
            xinxi.append(dianpu)
        num1 = 0
        for i in range(num - 20):
            if xinxi[i] not in shulian:
                shulian[xinxi[i]] = 0
                num1 += 1
        for i in range(num - 20):
            if (xinxi[i] in shulian):
                s = shulian.get(xinxi[i])
                s += 1
                shulian[xinxi[i]] = s
        temp = sorted(shulian.items(), key=lambda x: x[1], reverse=True)  # 按照字典value降序排列
        dianpu = []
        baifeng = []
        for i in range(10):
            dianpu.append(temp[i][0])
            baifeng.append(temp[i][1])
        print(dianpu)
        print(baifeng)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
        plt.figure(figsize=(6, 9))  # 调节图形大小
        # 扇形图
        explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        plt.subplots(figsize=(10, 8))
        plt.pie(baifeng, explode=explode, labels=dianpu, autopct='%1.1f%%', shadow=False, startangle=90)
        plt.axis('equal')
        plt.savefig(dir + "—著名商家.png")
        plt.show()
        plt.close()
        #写入文件
        with open(dir + ".csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["商品名称", "商品价格", "网址", "店铺", "商品信息"])
            data = colect_mongodb.find({}, {'_id': 0, "商品名称": 1, "商品价格": 1, "网址": 1, "店铺": 1, "商品信息": 1})
            for i in data:
                name0 = i.get('商品名称')
                name = "".join(name0.split())
                price = i.get('商品价格')
                url0 = i.get('网址')
                url = "".join(url0.split())
                dianpu0 = i.get('店铺')
                dianpu = "".join(dianpu0.split())
                xinxi0 = i.get('商品信息')
                xinxi = "".join(xinxi0.split())
                writer.writerow([name, price, url, dianpu, xinxi])
