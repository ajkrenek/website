# Generated by Django 4.1 on 2022-08-27 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('subreddit', models.CharField(max_length=200)),
                ('tumblr', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=200)),
            ],
        ),
    ]
