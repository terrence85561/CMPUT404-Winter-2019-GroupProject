from django.test import Client, TestCase
from django.urls import reverse
import uuid
import json
from myBlog.models import Author,Post,Comment,Friend
from django.contrib.auth.models import User
import datetime

class TestFriend(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser1')
        self.user.set_password('test')
        self.user.save()
        self.client = Client()
        self.client.login(username='testuser1',password='test')
        self.author = Author.objects.create(user=self.user,displayName='author',
                                            github='https://github.com/terrence8556',
                                            host='http://127.0.0.1:8000')

        # create another author client
        self.other_user = User.objects.create(username='testuser2')
        self.other_user