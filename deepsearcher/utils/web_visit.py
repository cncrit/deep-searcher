# -*- coding: utf-8 -*-
'''
#Author: Yalei Meng  yaleimeng@sina.com
#License: Created with VS Code, (C) Copyright 2025
#Description: 提供了百度、搜狗和360搜索的访问功能。
#Date: 
LastEditTime: 2025-04-15 13:30:34
#FilePath: Do not edit
'''
import requests as rq
from bs4 import BeautifulSoup as bs
from baidusearch.baidusearch import search


def html_in(page, load=None, soup=True,):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1", }
    if not load:
        r = rq.get(page, headers=head, timeout=9)
    else:
        r = rq.get(page, headers=head, timeout=9, params=load)
    # r.encoding = detect(r.content)['encoding']
    return bs(r.text, 'lxml') if soup else r.text


def search_sogou(query):
    '''测试成功。URL为跳转链接,默认9条结果'''
    alink = f'https://www.sogou.com/web?query={query}'
    soup = html_in(alink)
    # print(soup)
    piles = soup.select('div.vrwrap')
    data = []
    for pile in piles:
        if not pile.h3 or not pile.h3.a:
            continue
        # print(pile.h3)
        one = {'title': pile.h3.text, 'snippets': pile.text.strip().replace('\n', ''),
               'url': f'https://www.sogou.com{pile.h3.a['href']}', }
        data.append(one)
    return data


def search_360(query):
    '''测试成功。URL为跳转链接，默认10条结果'''
    soup = html_in(f'https://www.so.com/s?q={query}')
    piles = soup.select('li.res-list')
    data = []
    for pile in piles:
        if not pile.h3:
            continue
        one = {'title': pile.h3.text, 'snippets': pile.text.strip().replace('\n', ''),
               'url': pile.h3.a['href']}
        data.append(one)
    return data


def search_baidu(query):
    '''测试成功。URL为跳转链接，默认10条结果'''
    results = search(query, num_results=10)
    data = []
    for pile in results:
        one = {'url': pile['url'], 'title': pile['title'], 
            'snippets': pile['abstract'].replace('\n', ''),}
        data.append(one)
    return data


if __name__ == '__main__':
    chaxun = '2025五一放假安排'
    out1 = search_baidu(chaxun)
    # out1 =search_sogou(query)
    # out1 = search_360(query)
    print(out1)
    print(len(out1))