# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import expanddouban
from tt import html
import os
"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影' + ',' + category + ','+ location
    return url
"""
return a list of Movie objects with the given category and location.
"""
def getMovies(category, location):
    #html = expanddouban.getHtml(getMovieUrl(category, location))
    #html = requests.get(getMovieUrl(category, location)).text
    soup = BeautifulSoup(html, "html.parser")
    movie_list = soup.find(class_="list-wp")
    movie_list = movie_list.find_all("a")
    results = []
    for i in movie_list:
        name = i.p(class_="title")[0].get_text()
        rate = i.p(class_="rate")[0].get_text()
        location = location_tag
        category = category_tag
        info_link = i.get('href')
        cover_link = i.find('img').get('src')
        m = Movie(name, rate, location, category, info_link, cover_link)
        result = m.get_list()
        results.append(result)
    return results
class Movie(object):
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.rate = rate
        self.name = name
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link
    """
    组装成列表
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

category_tag = '悬疑'
location_tag = '法国'

print(getMovies(category_tag, location_tag))
Movie_lists = getMovies(category_tag, location_tag)
Dir = os.path.abspath('.')
Movie_csv = "movie.csv"
Ab_Movie_csv = os.path.join(Dir, Movie_csv)
with open(Ab_Movie_csv, 'w') as f:
    for n in range(len(Movie_lists)):
        element_num = len(Movie_lists[n])
        for movie_element in Movie_lists[n]:
            print(element_num)
            f.write(movie_element)
            element_num -= 1
            if element_num > 0:
                f.write(',')
            else:
                f.write('\n')
#print(Ab_Movie_csv)
