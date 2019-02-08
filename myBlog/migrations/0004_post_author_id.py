# Generated by Django 2.1.5 on 2019-02-07 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myBlog', '0003_auto_20190207_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
