import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup
from crawler_utils.utils import timer

results = {}
ids = 0
import csv

tasks = []


class Movie:
    def __init__(self, id, title, description, star, leader, tags, years, country, director_description, image_link, language, time_length, imdb_link):
        self.imdb_link = imdb_link
        self.time_length = time_length
        self.id = id
        self.star = star
        self.description = description
        self.title = title
        self.leader = leader
        self.tags = tags
        self.years = years
        self.country = country
        self.director_description = director_description
        self.image_link = image_link
        self.language = language


async def fetch(url, index):
    print('fetching url', url)
    async with aiohttp.ClientSession()as session:
        async with session.get(url) as response:
            assert response.status == 200
            print("this is index", index)
            return await response.text()


async def write_images(image_link, image_name):
    print('write images....', image_link)
    async with aiohttp.ClientSession()as session:
        async with session.get(image_link) as response:
            assert response.status == 200
            with open('movie_images/' + image_name + '.png', 'wb')as opener:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    opener.write(chunk)


async def parse_movie_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('span', {'property': 'v:itemreviewed'}).text
    image_link = soup.find('a', {'class': 'nbgnbg'}).find('img')['src']
    info = soup.find('div', {'id': 'info'})
    director = info.find_all('a', {'rel': 'v:directedBy'})[0].text
    leader = [a.text for a in info.find_all('a', {'rel': 'v:starring'})]
    tags = [a.text for a in info.find_all('span', {'property': 'v:genre'})]
    country = info.find('span', string='制片国家/地区:').next_sibling
    language = info.find('span', string='语言:').next_sibling
    show_time = info.find('span', {'property': 'v:initialReleaseDate'}).text
    time_length = info.find('span', {'property': 'v:runtime'}).text
    imdb_link = info.find('span', string='IMDb链接:').fetchNextSiblings()[0]['href']
    description = soup.find('span', {'property': 'v:summary'}).text
    star = soup.find('strong', {'property': 'v:average'}).text
    # comments = soup.find_all('div', {'class': 'comment-item'})
    return Movie(image_link=image_link, title=title, star=star, leader=leader, tags=tags, country=country, director_description=director, years=show_time, id=ids, description=description, time_length=time_length, imdb_link=imdb_link, language=language)


def write_movies(movie, index):
    print('write movies..')
    with open('movies_3.csv', 'a+')as opener:
        writer = csv.writer(opener)
        if opener.tell() == 0:
            writer.writerow(['id', 'title ', 'image_link ', 'country ', 'years ', 'director_description', 'leader', 'star ', 'description', 'tags', 'imdb', 'language', 'time_length', ''])
        writer.writerow([index, movie.title, movie.image_link, movie.country, movie.years, movie.director_description, movie.leader, movie.star, movie.description, '/'.join(movie.tags), movie.imdb_link, movie.language, movie.time_length])


async def get_results(index, url, parser):
    html = await fetch(url, index)
    movies = await parser(html)
    write_movies(movies, index)


async def handle_tasks(work_queue, parser):
    while not work_queue.empty():
        index, current_url = await work_queue.get()
        current_url = current_url[0]
        print('index', current_url, index)
        try:
            await get_results(index, current_url, parser)
        except Exception as e:
            logging.exception('Error for {}'.format(current_url), exc_info=True)


@timer
def envent_loop():
    q = asyncio.Queue()
    with open('movie_links.csv', 'r')as opener:
        reader = csv.reader(opener)
        for index, link in enumerate(reader):
            q.put_nowait((index, link))
    loop = asyncio.get_event_loop()
    tasks.append(handle_tasks(q, parse_movie_page))
    loop.run_until_complete(asyncio.wait(tasks))


envent_loop()
