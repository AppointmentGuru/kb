# Generated by Django 4.0.1 on 2022-02-04 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0005_article_search_phrases_category_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='mobile_video_embed_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='mobile_video_thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='mobile_video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='video_thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=1000),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=144, null=True)),
                ('slug', models.SlugField(max_length=144, null=True, unique=True)),
                ('icon', models.URLField(blank=True, null=True)),
                ('cover_image', models.URLField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('published', models.BooleanField(db_index=True, default=False)),
                ('order', models.PositiveIntegerField(db_index=True, default=1000)),
                ('upvotes', models.PositiveBigIntegerField(db_index=True, default=0)),
                ('downvotes', models.PositiveBigIntegerField(db_index=True, default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('articles', models.ManyToManyField(blank=True, to='help.Article')),
            ],
        ),
    ]
