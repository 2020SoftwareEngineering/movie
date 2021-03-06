# Generated by Django 2.2.10 on 2020-05-14 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200514_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=255, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='country',
            field=models.CharField(max_length=255, verbose_name='国家'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='d_rate',
            field=models.CharField(max_length=255, verbose_name='豆瓣评分'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=255, verbose_name='导演名称'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='leader',
            field=models.CharField(max_length=255, verbose_name='主演'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='电影名称'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='pic',
            field=models.FileField(max_length=255, upload_to='movie_cover', verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='years',
            field=models.CharField(max_length=255, verbose_name='年份'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=255, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='名字'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True, verbose_name='账号'),
        ),
    ]
