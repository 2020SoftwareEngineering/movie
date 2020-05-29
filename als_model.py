import os
import shutil

import pandas as pd
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel
from pyspark.sql import SparkSession

# from pyspark import
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")
import django

django.setup()

from user.models import Rate, Movie

os.environ['SPARK_HOME'] = '/usr/local/Cellar/apache-spark/2.4.5/libexec'


def load_all_ratings(min_ratings=1):
    # 从数据库提取相关列的数据
    columns = ['user_id', 'movie_id', 'mark']
    ratings_data = Rate.objects.all().values(*columns)
    print('count', ratings_data.count())
    ratings = pd.DataFrame.from_records(ratings_data, columns=columns)
    ratings['user_id'] = ratings['user_id'].astype(int)
    ratings['movie_id'] = ratings['movie_id'].astype(int)
    ratings['mark'] = ratings['mark'].astype(float)
    return ratings


def als_recommend_by_user_id(user_id):
    model = AlsModel()
    model.load_model()
    # print('user feature',model.als.userFeatures().count(),model.als.userFeatures().collectAsMap())
    # print('product feature',(model.als.productFeatures().values()))
    res = model.als.recommendProducts(user_id, 30)
    movie_list = []
    for rating in res:
        movie_id = rating.product
        is_watched = Rate.objects.filter(user_id=user_id, movie_id=movie_id).first()
        if is_watched is None:
            movie = Movie.objects.filter(id=movie_id).first()
            if movie not in movie_list:
                movie_list.append(movie)
    return movie_list


# sys.path.append('/usr/local/Cellar/apache-spark/2.4.5/libexec')
# sys.path.append('D:\spark-3.0.0-preview2-bin-hadoop2.7\python')
# als_model_path='../data/als-m'
class AlsModel(object):
    _instance = None
    als = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, k=10):
        self.k = k
        self.spark = SparkSession.builder.appName("movie").enableHiveSupport().getOrCreate()

    def build(self, data):
        print('this is data', data)
        sparkDF = self.spark.createDataFrame(data)
        als = ALS.train(sparkDF, self.k, 5)
        self.als = als
        self.save_model(self.spark.sparkContext, als)
        return als

    def save_model(self, sc, model):
        """存储模型"""
        # try:
        path = "./model_data/als-model"
        try:
            shutil.rmtree('./model_data/als-model/metadata', ignore_errors=True)
            shutil.rmtree('./model_data/als-model/data', ignore_errors=True)
        except FileNotFoundError:
            pass
        model.save(sc, path)
        print('save success')
        # except Mo Exception:
        # print("模型已存在,先删除后创建")
        return model

    def train(self):
        data = load_all_ratings()
        return self.build(data=data)

    def load_model(self):
        sc = self.spark.sparkContext
        try:
            model = MatrixFactorizationModel.load(sc, "./model_data/als-model")
            self.als = model
            print('载入成功!')
            return model
        except Exception:
            print("模型不存在, 请先训练模型")
            return self.train()


if __name__ == '__main__':
    load_all_ratings()
    als_recommend_by_user_id(21)
