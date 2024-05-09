# -*- coding: utf-8 -*- 
"""
Author: JerryLaw
Time: 2024/4/18 9:56
Email: 623487850@qq.com
"""
import redis
from rediscluster import RedisCluster

from common.readLog import logs


class OperateRedis:
    def __init__(self, env, host, port, password, db):
        '''

        :param env: 运行环境
        :param host: ip
        :param port: 端口
        :param password: 密码
        :param db: 数据库
        '''
        self.env = env
        self.host = host
        self.port = port
        self.password = password
        self.db = db

    def __connect_redis(self):
        try:
            if self.env == "dev":
                logs.info("连接redis,host:{0},port:{1},password:{2},db:{3}".format(self.host, self.port,
                                                                                   self.password, self.db))
                self.con = redis.StrictRedis(host=self.host, port=self.port, password=self.password, db=self.db)
                logs.info("连接redis成功")
            elif self.env == "fat":
                startup_nodes = []
                for port in self.port.split(","):
                    startup_nodes.append({"host": self.host, "port": port})
                logs.info("连接redis,集群:{0},password:{1},db:{2}".format(startup_nodes, self.password, self.db))
                self.con = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, password=self.password)
                logs.info("连接redis成功")
            return self.con
        except Exception as e:
            logs.error(e)

    def get(self, key):
        try:
            self.__connect_redis()
            value = self.con.get(key)
            if value:
                if isinstance(value, bytes):
                    result = value.decode()
                else:
                    result = value
            else:
                result = "The key is incorrect or does not exist..."
            logs.info("key:{0},value:{1}".format(key, result))
            return result
        except Exception as e:
            logs.error(e)
        finally:
            self.con.close()
            logs.info("关闭redis连接")
