from django.test import Client, TestCase
from django.urls import reverse
import uuid
import json
from myBlog.models import Author,Post,Comment,Friend
from django.contrib.auth.models import User
import datetime



class TestViews(TestCase):
    def setUp(self):
        # https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        # create first user author client
        self.user = User.objects.create(username='testuser1')
        self.user.set_password('test')
        self.user.save()
        self.client = Client()
        self.client.login(username='testuser1', password='test')
        self.author = Author.objects.create(user=self.user, displayName='author1',
                                            github='https://github.com/terrence85561')

        # create another user author client
        self.other_user = User.objects.create(username='testuser2')
        self.other_user.set_password('test')
        self.other_user.save()
        self.other_client = Client()
        self.other_client.login(username='testuser2',password='test')
        self.other_author = Author.objects.create(user=self.other_user,displayName='author2',
                                                  github='https://github.com/terrence85561')

        self.new_post_url = reverse('new_post')
        self.post_to_user_url = reverse('posttouser')

    def test_New_Post_Handler_POST_API(self):
        response = self.client.post(self.new_post_url,{
            'title': 'POST1',
            'description': 'post for testing',
            'contentType': 'text/plain',
            'author':{
                'id':self.author.id,
                'host':self.author.host,
                'displayName':self.author.displayName,
                'github':self.author.github
            },
            'visibility': 'PUBLIC',
            'content': 'test'
        },'application/json')
        self.assertEquals(response.status_code, 200)

    def test_Post_Handler_GET_OTHER_AUTHOR_POST_API(self):
        # test of post_handler class
        # test get other author's post
        self.other_client.post(self.new_post_url,{
                'title': 'original post1',
                'content': 'This is a test post',
                'categories': 'test',
                'contentType': 'text/plain',
                'author': {
                    'id':self.other_author.id,
                    'host':self.other_author.host,
                    'displayName':self.other_author.displayName,
                    'github':self.other_author.github
                },
                'visibility': 'PUBLIC',
                'description': 'test description'

        },'application/json')

        post1 = Post.objects.get(title='original post1')
        post1_postid = post1.postid
        modify_post_url = reverse('modify_post',args=[post1_postid])

        response = self.client.get(modify_post_url)

        self.assertEquals(response.status_code,200)

    def test_Post_Handler_GET_MY_POST_API(self):
        # test visit my post and it is private to me
        self.client.post(self.new_post_url,{
            'title': 'my post',
            'content': 'This is my post',
            'categories': 'test',
            'contentType': 'text/plain',
            'author':{
                'id':self.author.id,
                'host':self.author.host,
                'displayName':self.author.displayName,
                'github':self.author.github
            },
            'visibility': 'PRIVATE',
            'description': 'test description'
        },'application/json')

        post1 = Post.objects.get(title='my post')
        post1_postid = post1.postid
        modify_post_url = reverse('modify_post',args=[post1_postid])
        response = self.client.get(modify_post_url)
        self.assertEquals(response.status_code,200)

        # test other user cannot visit my post
        other_response = self.other_client.get(modify_post_url)
        self.assertEquals(other_response.status_code,404)

    def test_Post_Handler_PUT_API(self):
        # first create a public post, test other user can see it or not
        # then modified to private and change title, test title, test status code,
        # test other user can see it or not

        # create a post
        self.client.post(self.new_post_url,{
            'title': 'original post2',
            'content': 'This is a test post',
            'categories': 'test',
            'contentType': 'text/plain',
            'author':{
                'id':self.author.id,
                'host':self.author.host,
                'displayName':self.author.displayName,
                'github':self.author.github
            },
            'visibility': 'PUBLIC',
            'description': 'test description'
        },'application/json')
        obj = Post.objects.get(title='original post2')
        post1_postid = obj.postid
        modify_post_url = reverse('modify_post',args=[post1_postid])
        response_get=self.other_client.get(modify_post_url)
        self.assertEquals(response_get.status_code,200)

        response = self.client.put(modify_post_url,json.dumps({
            'title': 'modified my title',
            'visibility': 'PRIVATE',
            'description': 'test description',
            'contentType': 'text/plain',
            'content': 'This is a test post'
        }),content_type='application/json')
        self.assertEquals(response.status_code,200)
        # emmmm...
        post = Post.objects.get(pk=post1_postid)
        self.assertEquals(post.title,'modified my title')
        response_get=self.other_client.get(modify_post_url)
        self.assertEquals(response_get.status_code,404)

    def test_Post_Handler_DELETE_API(self):
        # create a post first, test status code == 204
        # test if the post still exist, test if other user can delete it

        # create a public post
        self.client.post(self.new_post_url,{
            'title': 'need delete',
            'content': 'This is my post',
            'categories': 'test',
            'contentType': 'text/plain',
            'author':{
                'id':self.author.id,
                'host':self.author.host,
                'displayName':self.author.displayName,
                'github':self.author.github
            },
            'visibility': 'PUBLIC',
            'description': 'test description'
        },'application/json')
        post = Post.objects.get(title='need delete')
        post_id = post.postid
        modify_post_url = reverse('modify_post', args=[post_id])

        # test if other user can delete it or not
        response = self.other_client.delete(modify_post_url)
        self.assertEquals(response.status_code, 404)

        # test if current user can delete it or not
        response1 = self.client.delete(modify_post_url)
        self.assertEquals(response1.status_code, 204)

        # test if the post still exist or not
        self.assertFalse(Post.objects.filter(pk=post_id).exists())

    def test_Comment_Handler_POST_API(self):
        # create a public post first , then test if user can add comment on it
        # then create a private post, then test if user can add comment on it.

        # create a public post
        self.other_client.post(self.new_post_url,{
            'title': 'comment this post!',
            'content': 'please make some comments',
            'categories': 'test',
            'contentType': 'text/plain',
            'author':{
                'id':self.other_author.id,
                'host':self.other_author.host,
                'displayName':self.other_author.displayName,
                'github':self.other_author.github
            },
            'visibility': 'PUBLIC',
            'description': 'test description'
        },'application/json')
        post = Post.objects.get(title='comment this post!')
        post_id = post.postid

        # create a comment on this post
        # get the reverse url
        comment_url = reverse('comment', args=[post_id])
        response=self.client.post(comment_url, {
            'query': 'addComment',
            'post': 'testserver',
            'comment': {
                'author': {
                    'id': self.author.id,
                    'host': 'xxx',
                    'displayName': self.author.displayName,
                    'url': 'xxx',
                    'github': self.author.github
                },
                'comment': 'this is my first comment',
                'contentType': 'text/plain',
                'published': datetime.datetime.now(),
            }
        },'application/json')
        self.assertEquals(response.status_code,200)
        #self.assertEquals(response.status_code,400)

        # create a private post
        self.other_client.post(self.new_post_url,{
            'title': 'comment this private post',
            'content': 'please make some comments',
            'categories': 'test',
            'contentType': 'text/plain',
            'author':{
                'id':self.other_author.id,
                'host':self.other_author.host,
                'displayName':self.other_author.displayName,
                'github':self.other_author.github
            },
            'visibility': 'PRIVATE',
            'description': 'test description'
        },'application/json')
        post1 = Post.objects.get(title='comment this private post')
        post1_id = post1.postid

        comment_url_private = reverse('comment',args=[post1_id])
        response1=self.client.post(comment_url_private,{
            'query': 'addComment',
            'post': 'testserver',
            'comment': {
                'author': {
                    'id': self.author.id,
                    'host': 'xxx',
                    'displayName': self.author.displayName,
                    'url': 'xxx',
                    'github': self.author.github
                },
                'comment': 'this is comment from author1',
                'contentType': 'text/plain',
                'published': datetime.datetime.now(),
            }
        },'application/json')
        self.assertEquals(response1.status_code,403)

        response2 = self.other_client.post(comment_url_private, {
            'query': 'addComment',
            'post': 'testserver',
            'comment': {
                'author': {
                    'id': self.other_author.id,
                    'host': 'xxx',
                    'displayName': self.other_author.displayName,
                    'url': 'xxx',
                    'github': self.other_author.github
                },
                'comment': 'this is comment from author2',
                'contentType': 'text/plain',
                'published': datetime.datetime.now(),
            }
        },'application/json')

        self.assertEquals(response2.status_code,200)

    def test_Comment_Handler_GET_API(self):
        # first, post a post, add comments on it, then test if we can get the comments

        # create a post
        self.client.post(self.new_post_url,{
            'title': 'make some comments',
            'content': 'please make some comments',
            'categories': 'test',
            'contentType': 'text/plain',
            'author':{
                'id':self.author.id,
                'host':self.author.host,
                'displayName':self.author.displayName,
                'github':self.author.github
            },
            'visibility': 'PUBLIC',
            'description': 'test description'
        },'application/json')

        # get the post id for this post
        post = Post.objects.get(title='make some comments')
        post_id = post.postid

        # add comments on this post
        comment_url = reverse('comment',args=[post_id])
        self.other_client.post(comment_url,{
            'query': 'addComment',
            'post': 'testserver',
            'comment': {
                'author': {
                    'id': self.other_author.id,
                    'host': 'xxx',
                    'displayName': self.other_author.displayName,
                    'url': 'xxx',
                    'github': self.other_author.github
                },
                'comment': 'this is comment from author2',
                'contentType': 'text/plain',
                'published': datetime.datetime.now(),
            }

        },'application/json')

        # test if user can get this comment
        response = self.client.get(comment_url)
        self.assertEquals(response.status_code,200)
        content = json.loads(response.content)
        self.assertEquals(content['comments'][0]['comment'],'this is comment from author2')

    def test_Post_To_User_HandlerView(self):
        # one author creates some posts and adds some comments on them.
        # another author tries to visit all these posts

        posts_num = 10
        # post ten posts and get a list of these posts' ids.
        for i in range(posts_num):
            self.client.post(self.new_post_url, {
                'title': 'post'+str(i),
                'content': 'please make some comments on post'+str(i),
                'categories': 'test',
                'contentType': 'text/plain',
                'author':{
                'id':self.author.id,
                'host':self.author.host,
                'displayName':self.author.displayName,
                'github':self.author.github
            },
                'visibility': 'PUBLIC',
                'description': 'test description'
            },'application/json')

            post = Post.objects.get(title='post'+str(i))
            post_id = post.postid
            comment_url = reverse('comment', args=[post_id])
            # add five comments on this post
            for j in range(5):
                self.client.post(comment_url,{
                    'query': 'addComment',
                    'post': 'testserver',
                    'comment': {
                        'author': {
                            'id': self.author.id,
                            'host': 'xxx',
                            'displayName': self.author.displayName,
                            'url': 'xxx',
                            'github': self.author.github
                        },
                        'comment': 'comment on post'+str(i),
                        'contentType': 'text/plain',
                        'published': datetime.datetime.now(),
                    }

                }, 'application/json')

        # another author tries to visit all posts
        response = self.other_client.get(self.post_to_user_url,{'page':2,'size':1})
        content = json.loads(response.content)

        self.assertEquals(response.status_code,200)

        # test another author visit all posts created by a userid
        post_to_userid_url = reverse('posttouserid',args=[self.author.id])
        response1 = self.other_client.get(post_to_userid_url)
        content = json.loads(response1.content)
        self.assertEquals(response1.status_code,200)


