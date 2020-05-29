# 添加和读取数据到数据库中
import ast
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()
import csv
from user.models import Movie, Tags

opener = open('movies_3.csv', 'r', encoding='utf-8')
reader = csv.reader(opener)
next(reader)

for line in reader:
    if len(line) == 0:
        continue
    id, title, image_link, country, years, director_description, leader, star, description, tags, imdb, language, time_length = line
    tags = tags.split('/')
    leader = '/'.join(ast.literal_eval(leader))
    pic_name = 'movie_cover/' + title.replace('/', '_')+'.png'
    movie, created = Movie.objects.get_or_create(name=title, defaults={'pic': pic_name, 'country': country, 'years': years, 'leader': leader, 'd_rate_nums': 0, 'd_rate': star, 'intro': description, 'director': director_description})
    print(movie, 'created: ', created)
    for tag in tags:
        tag_obj, created = Tags.objects.get_or_create(name=tag)
        movie.tags.add(tag_obj)
