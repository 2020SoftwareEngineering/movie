# Generated by Django 2.2.10 on 2020-05-21 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_like_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='LikeComment',
        ),
    ]
