
class shuru:
    def __init__(self,search_n):
        self.url="https://search.jd.com/Search?&enc=utf-8&pvid=83d510b54d2c4b40ba7f31eebf12fbe2"
        self.dir=search_n
    def geturl(self):
        return self.url
    def getdir(self):
        return self.dir