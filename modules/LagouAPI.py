#!/usr/bin/env python
# coding=utf-8

import datetime
import copy
import requests
import urllib.parse
from bs4 import BeautifulSoup

from modules.GaodeMapAPI import GaodeMapAPI
# from GaodeMapAPI import GaodeMapAPI

class LagouAPI(object):
    LAGOU_GATEWAY = 'http://www.lagou.com/jobs/positionAjax.json?'
    sess = requests.Session()

    @classmethod
    def search(cls, kd, **kwargs):
        url_encoded = urllib.parse.urlencode(kwargs)
        cls.jl_url = cls.LAGOU_GATEWAY + url_encoded
        page = 1
        page_max = None
        while True:
            payload = {
                "first": False,
                'pn': page,
                'kd': kd,
            }
            headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            cookies = dict(
                    user_trace_token="20170111190001-2bfa23acde1148f880a527658ea1617c",
                    LGUID="20170111190001-19b03195-d7ed-11e6-a1c2-525400f775ce",
                )
            r = cls.sess.post(cls.jl_url, data=payload, cookies=cookies, headers=headers) 
            json_result = r.json()
            # print(json.dumps(json_result, indent=4, ensure_ascii=False))
            if page_max is None:
                page_max = json_result['content']['positionResult']['totalCount']
            for j in json_result['content']['positionResult']['result']:
                yield j
            if page >= page_max:
                break
            page += 1

    @classmethod
    def get_location_by_pos_id(cls, pos_id):
        """
        抓取网页内容，分析并返回公司位置
        """
        cookies = dict(user_trace_token="20170111190001-2bfa23acde1148f880a527658ea1617c",
            LGUID="20170111190001-19b03195-d7ed-11e6-a1c2-525400f775ce",
            )
        r = cls.sess.get('http://www.lagou.com/jobs/%d.html' % pos_id, cookies=cookies)
        soup = BeautifulSoup(r.content, "html.parser")
        corp_info = soup.select('div[class="work_addr"]')
        a = corp_info[0].get_text()

        return a.strip().replace(' ', '').replace('-','')[:-6].split('\n')


def GetJob():

    job = {}
    jobs = {"items": []}
    
    for jd in LagouAPI.search('Python', city='上海', gx='全职', yx='15k-25k'):
        address = ''.join(LagouAPI.get_location_by_pos_id(jd['positionId']))
        # address = ''.join(address)
        job['address'] = address
        try:
            job['longitude'], job['latitude'] = GaodeMapAPI.search(address).split(',')
        except:
            continue
        job['positionName'] = jd['positionName']
        job['companyShortName'] = jd['companyShortName']
        job['salary'] = jd['salary']
        job['companySize'] = jd['companySize']
        job['createTime'] = jd['createTime']
        job['positionId'] = jd['positionId']
        job['financeStage'] = jd['financeStage']

        jobs["items"].append(copy.copy(job))
        job.clear()

    return jobs

