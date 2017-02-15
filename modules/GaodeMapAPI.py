#!/usr/bin/env python
# coding=utf-8

import functools
import requests

class GaodeMapAPI(object):
    """
    返回经纬度
    """
    GAODE_GATEWAY = 'http://restapi.amap.com/v3/geocode/geo?'
    GAODE_API_KEY = '1ca233cdb2e822adcbf44207689d4dd0'
    sess = requests.Session()

    @classmethod
    @functools.lru_cache(65536)
    def search(cls, loc):
        q = 'address=%soutput=XML&key=%s' % (loc, cls.GAODE_API_KEY)
        ret = cls.sess.get(cls.GAODE_GATEWAY + q).json()
        if ret['status'] == '1':
            try:
                return(ret['geocodes'][0]['location'])
            except IndexError as e:
                return None
        return None

if __name__ == '__main__':
    ret = GaodeMapAPI.search("上海浦东新区张江碧波路690号")


