from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render,get_list_or_404
from .models import Post, Author, Comment, Friend
from .serializers import PostSerializer, CommentSerializer, AuthorSerializer, CustomPagination, FriendSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from . import Helpers

class CommentHandler(APIView):
    def get(self, request, postid, format=None):
        post = Post.objects.get(pk=postid)
        if (not Helpers.verify_current_user_to_post(post, request)):
            responsBody={
                "query": "addComment",
                "success":False,
                "message":"Comment not allowed"
                }
            return Response(responsBody, status=403)
        else:
            current_user_uuid = Helpers.get_current_user_uuid(request)
            comments_list = get_list_or_404(Comment,postid=postid)
            paginator = CustomPagination()
            results = paginator.paginate_queryset(comments_list, request)
            serializer=CommentSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request, postid, format=None):
        data = request.data
        if data['query'] == 'addComment':
            post = Post.objects.get(pk=postid)
            if (not Helpers.verify_current_user_to_post(post, request)):
                responsBody={
                    "query": "addComment",
                    "success":False,
                    "message":"Comment not allowed"
                    }
                return Response(responsBody, status=403)
            else:
                current_user_uuid = Helpers.get_current_user_uuid(request)
                data = {'comment':request.data['comment']['comment'], 'contentType':request.data['comment']['contentType']}
                serializer = CommentSerializer(data=data, context={'author': request.data['comment']['author'], 'postid':postid})
                if serializer.is_valid():
                    serializer.save()
                    responsBody={
                    "query": "addComment",
                    "success":True,
                    "message":"Comment Added"
                    }
                    return Response(responsBody, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not sending the new comment with the correct format. Missing 'query': 'addComment'",status=status.HTTP_400_BAD_REQUEST)
 