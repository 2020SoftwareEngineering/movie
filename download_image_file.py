# 添加和读取数据到数据库中
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")
import threading

django.setup()
from user.models import Movie
import requests

exist = os.listdir('media')
exist_dict = {}
print(exist)
for e in exist:
    exist_dict[e.split('.')[0]] = e
print(exist_dict)
movies = Movie.objects.all().values('pic', 'name')
url_list = [movie for movie in movies if movie['pic'].startswith('http')]
user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"

headers = {'User-Agent': user_agent}


# session = requests.session()
# session.headers = {'user-agent': user_agent}


def download_image():
    url = url_list.pop()
    name = url.get('name')
    url = url['pic']
    pic_name = name.replace('/', '_')
    if exist_dict.get(pic_name):
        print('命中缓存!', name)
        return
    print('replaced name')
    res = requests.get(url, headers=headers)
    assert res.status_code == 200

    with open('media/' + pic_name + '.png', 'wb')as opener:
        opener.write(res.content)
    print('写入成功!', pic_name)


while url_list:
    for i in range(5):
        th1 = threading.Thread(target=download_image)
        th1.start()
        th1.join()
