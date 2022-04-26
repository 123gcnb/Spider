import pymongo
import redis
class connectdb:
    def __init__(self,search_n):
        self.search_n=search_n
        # 连接mongodb
        self.client_mongodb = pymongo.MongoClient()
        self.db_mongodb = self.client_mongodb['data']
        self.colect_mongodb1 = self.db_mongodb[self.search_n]
        self.colect_mongodb1.drop()
        self.colect_mongodb=self.db_mongodb[self.search_n]
        # 连接redis
        self.client_redis = redis.StrictRedis()
        #清空缓存
        self.client_redis.flushall()
    def get_colect_mongodb(self):
        return self.colect_mongodb
    def get_client_redis(self):
        return self.client_redis