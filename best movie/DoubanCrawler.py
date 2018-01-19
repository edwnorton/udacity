# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import expanddouban
import os
import csv
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
            m = Movie(name, rate, location, category, info_link, cover_link)
            result = m.get_list()
            result_tag.append(result)
        m = result_tag
        results_all = results_all + m
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
def Movie_count():
    """
    按类型标签建立统计电影地区数量的字典
    :return: movie_dic_tag and tag_count
    """
    global tag0_count, tag1_count, tag2_count
    for i in movies:
        if i[3] == category_tag[0]:
            tag0_count += 1  # 悬疑类型电影总计数
            if i[2] not in movie_dic_tag0:
                movie_dic_tag0[i[2]] = 1  # 按地区计数
            else:
                movie_dic_tag0[i[2]] += 1
        elif i[3] == category_tag[1]:
            tag1_count += 1
            if i[2] not in movie_dic_tag1:
                movie_dic_tag1[i[2]] = 1
            else:
                movie_dic_tag1[i[2]] += 1
        elif i[3] == category_tag[2]:
            tag2_count += 1
            if i[2] not in movie_dic_tag2:
                movie_dic_tag2[i[2]] = 1
            else:
                movie_dic_tag2[i[2]] += 1
        else:
            pass
    return

category_tag = ['悬疑', '恐怖', '犯罪']
location_tag = []
Movie_lists = getMovies(category_tag, location_tag)
csv_file(Movie_lists)
"""
output.txt file
"""
with open('movie.csv', 'r') as f:
    reader = csv.reader(f)
    movies = list(reader)
movie_dic_tag0 = {}
movie_dic_tag1 = {}
movie_dic_tag2 = {}
tag0_count = 0
tag1_count = 0
tag2_count = 0
Movie_count()
#print(movie_dic_tag0, movie_dic_tag1, movie_dic_tag2)
tag0_sorted = sorted(movie_dic_tag0.items(), key=lambda item: item[1], reverse=True)
tag1_sorted = sorted(movie_dic_tag1.items(), key=lambda item: item[1], reverse=True)
tag2_sorted = sorted(movie_dic_tag2.items(), key=lambda item: item[1], reverse=True)
Tag_0 = "In the \"{}\" category, top three region are: 1.{}, 2.{}, 3.{}\nThe percentage of total movies in this category are:{:.1f}%, {:.1f}%, {:.1f}%".format(category_tag[0], tag0_sorted[0][0], tag0_sorted[1][0], tag0_sorted[2][0], 100*(tag0_sorted[0][1]/tag0_count), 100*(tag0_sorted[1][1]/tag0_count), 100*(tag0_sorted[2][1]/tag0_count))
Tag_1 = "In the \"{}\" category, top three region are: 1.{}, 2.{}, 3.{}\nThe percentage of total movies in this category are:{:.1f}%, {:.1f}%, {:.1f}%".format(category_tag[1], tag1_sorted[0][0], tag1_sorted[1][0], tag1_sorted[2][0], 100*(tag1_sorted[0][1]/tag1_count), 100*(tag1_sorted[1][1]/tag1_count), 100*(tag1_sorted[2][1]/tag1_count))
Tag_2 = "In the \"{}\" category, top three region are: 1.{}, 2.{}, 3.{}\nThe percentage of total movies in this category are:{:.1f}%, {:.1f}%, {:.1f}%".format(category_tag[2], tag2_sorted[0][0], tag2_sorted[1][0], tag2_sorted[2][0], 100*(tag2_sorted[0][1]/tag2_count), 100*(tag2_sorted[1][1]/tag2_count), 100*(tag2_sorted[2][1]/tag2_count))
with open('output.txt', "w") as f:
    f.write(Tag_0 + "\n")
    f.write(Tag_1 + "\n")
    f.write(Tag_2 + "\n")
