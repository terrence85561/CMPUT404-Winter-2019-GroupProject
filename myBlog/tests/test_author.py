from django.test import Client, TestCase
from django.urls import reverse
import uuid
import json
from myBlog.models import Author,Post,Comment,Friend
from django.contrib.auth.models import User
import datetime

class TestAuthor(TestCase):
    def setUp(self):
        pass