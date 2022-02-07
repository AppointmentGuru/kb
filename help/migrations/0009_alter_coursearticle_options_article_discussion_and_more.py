# Generated by Django 4.0.1 on 2022-02-07 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0008_course_articles'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursearticle',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='article',
            name='discussion',
            field=models.TextField(blank=True, help_text='Admin only field for discussion on the article', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='keywords',
            field=models.TextField(blank=True, help_text='Meta Keywords for SEO', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='keywords',
            field=models.TextField(blank=True, help_text='Meta Keywords for SEO', null=True),
        ),
        migrations.AddField(
            model_name='coursearticle',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
