# Generated by Django 4.0.1 on 2022-02-04 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0007_remove_course_articles_coursearticle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='articles',
            field=models.ManyToManyField(blank=True, through='help.CourseArticle', to='help.Article'),
        ),
    ]
