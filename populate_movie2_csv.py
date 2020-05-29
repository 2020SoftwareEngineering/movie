# 添加和读取数据到数据库中
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()
import csv

opener = open('movies_2.csv', 'r', encoding='utf-8')
reader = csv.reader(opener)
next(reader)

for line in reader:
    if len(line) == 0:
        continue
    print(line)
    print(len(line))
    id, name, picture, country, year, director, leader, star, description, tags, _ = line
    tags = tags.replace('/','')
    print(tags)
    continue

    movie = Movie.objects.create(name=name, pic=name, country=country, years=year, leader=leader, d_rate_nums=star, d_rate=star, intro=description, director=director)

    print(tags)
    for tag in tags:
        tag_obj, created = Tags.objects.get_or_create(name=tag)
        print('created', created)
        movie.tags.add(tag_obj.id)
