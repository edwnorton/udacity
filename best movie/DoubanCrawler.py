# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import expanddouban
#from tt import html
import os
def splice_tag(url_str, tag_list):
    n = len(tag_list)
    if n>0:
        url_str = url_str + tag_list + ','
    else:
        pass
    return url_str
"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,'
    Urllist = []
    c_len = len(category)
    l_len = len(location)
    if l_len > 0:#如果location的list不为空，循环拼接tag组成url并加入Urllist
        for i in range(len(location)):
            if c_len > 0:
                url_tr = url + location[i] + ','
                for j in range(len(category)):
                    if c_len > 0:
                        urllist = url_tr + category[j]
                        Urllist.append(urllist)
                    else:
                        urllist = url_tr[:-1]
                        Urllist.append(urllist)
            else:
                url_tr = url + location[i]
                Urllist.append(url_tr)
    else:
        for i in range(len(category)):
            if c_len > 0:
                url_tr = url + category[i]
                Urllist.append(url_tr)
            else:
                url_tr = url[:-1]
                Urllist.append(url_tr)
    return Urllist
"""
return a list of Movie objects with the given category and location.
"""
def getMovies(category, location):
    Url_list = getMovieUrl(category, location)
    results_all = []
    for url in Url_list:
        html = expanddouban.getHtml(url)
        #html = requests.get(getMovieUrl(category, location)).text
        soup = BeautifulSoup(html, "html.parser")
        movie_list = soup.find(class_="list-wp")
        movie_list = movie_list.find_all("a")
        result_tag = []
        for i in movie_list:  # 解析html获取需要的元素
            movie_tag = soup.find_all("ul", class_="category")
            category_name = movie_tag[1].find(class_="tag-checked tag").get_text()
            name = i.p(class_="title")[0].get_text()
            rate = i.p(class_="rate")[0].get_text()
            category = category_name
            info_link = i.get('href')
            cover_link = i.find('img').get('src')
            movie_info_html = expanddouban.getHtml(info_link)
            info_soup = BeautifulSoup(movie_info_html, "html.parser")
            a = info_soup.find_all("div", id="info")
            patt = ".*制片国家/地区:</span> (.*)<br/>"
            location_name = re.search(patt, str(a)).group(1)
            location = location_name
            print(a)
            print(location)
            m = Movie(name, rate, location, category, info_link, cover_link)
            result = m.get_list()
            result_tag.append(result)
        m = result_tag
        #print('m:', m)
        #print('before:result', results_all)
        results_all = results_all + m
        #print('after:result', results_all)
    return results_all
"""
定义电影类
"""
class Movie(object):
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.rate = rate
        self.name = name
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link
    """
    把电影每个元素拼接组装成列表
    """
    def get_list(self):
        result_list = []
        result_list.append(self.name)
        result_list.append(self.rate)
        result_list.append(self.location)
        result_list.append(self.category)
        result_list.append(self.info_link)
        result_list.append(self.cover_link)
        return result_list
def csv_file(Movie_lists):
    """
    输出csv文件
    """
    Dir = os.path.abspath('.')
    Movie_csv = "movie.csv"
    Ab_Movie_csv = os.path.join(Dir, Movie_csv)
    with open(Ab_Movie_csv, 'w') as f:
        for n in range(len(Movie_lists)):#从电影列表中取每条记录
            element_num = len(Movie_lists[n])
            for movie_element in Movie_lists[n]:#向文件中逐条写入每个元素
                f.write(movie_element)
                element_num -= 1
                if element_num > 0:
                    f.write(',')
                else:
                    f.write('\n')
    return

category_tag = ['悬疑', '恐怖', '犯罪']
location_tag = []
print(getMovieUrl(category_tag, location_tag))
print(getMovies(category_tag, location_tag))
Movie_lists = getMovies(category_tag, location_tag)
csv_file(Movie_lists)
#print(Ab_Movie_csv)
