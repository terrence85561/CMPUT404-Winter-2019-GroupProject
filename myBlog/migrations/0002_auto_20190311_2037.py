# Generated by Django 2.1.5 on 2019-03-12 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myBlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='myBlog.Author'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friend',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reciver', to='myBlog.Author'),
        ),
    ]
