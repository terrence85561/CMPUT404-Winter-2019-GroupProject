# Generated by Django 2.1.5 on 2019-03-21 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBlog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('host', models.URLField(primary_key=True, serialize=False)),
                ('shareImages', models.BooleanField(default=True)),
                ('sharePost', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=400)),
                ('password', models.CharField(max_length=400)),
            ],
        ),
    ]