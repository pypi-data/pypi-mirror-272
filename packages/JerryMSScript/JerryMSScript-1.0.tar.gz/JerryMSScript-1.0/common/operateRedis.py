# -*- coding: utf-8 -*- 
"""
Author: JerryLaw
Time: 2024/4/18 9:56
Email: 623487850@qq.com
"""
import redis
from rediscluster import RedisCluster
from common.readLog import logs
from typing import Union


class OperateRedis:
    def __init__(self, env="fat", host="127.0.0.1", port: Union[int, str] = None, password="admin", db=None):
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
                logs.info(f"连接redis,host:{self.host},port:{self.port},password:{self.password},db:{self.db}")
                self.con = redis.StrictRedis(host=self.host, port=self.port, password=self.password, db=self.db)
                logs.info("连接redis成功")
            elif self.env == "fat":
                startup_nodes = []
                for port in self.port.split(","):
                    startup_nodes.append({"host": self.host, "port": port})
                logs.info(f"连接redis,集群:{startup_nodes},password:{self.password},db:{self.db}")
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
            logs.info(f"key:{key},value:{result}")
            return result
        except Exception as e:
            logs.error(e)
        finally:
            self.con.close()
            logs.info("关闭redis连接")
