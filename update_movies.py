import os

import django
# 此脚本用来更新现有数据库

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()
from user.models import *

movies = Movie.objects.all()
for movie in movies:
    if movie.pic.startswith('movie_cover'):
        continue
    movie.pic = 'movie_cover/' + movie.pic
    movie.save()
