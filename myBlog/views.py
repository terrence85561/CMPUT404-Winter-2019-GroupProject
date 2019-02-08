from rest_framework_swagger.views import get_swagger_view
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render
from .models import Post
from .serializers import PostSerializer

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import generic

# Code from: Reference: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
# https://docs.djangoproject.com/en/2.1/topics/auth/default/
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username,password=password, is_active=False)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



# https://www.django-rest-framework.org/api-guide/views/

@login_required(login_url="home")
@api_view(['GET','POST', 'PUT', 'DELETE'])
def PostHandler(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
    	return Response(PostSerializer(post).data)
    elif request.method == 'POST':
    	return Response({"message": "POST method", "data": post})    
    elif request.method == 'PUT':
        return Response({"message": "PUT method", "data": request.data})
    elif request.method == 'DELETE':
        return Response({"message": "DELETE Method", "data": request.data})


@login_required(login_url="home")
@api_view(['GET','POST', 'PUT', 'DELETE'])
def CommentHandler(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
    	return Response(PostSerializer(post).data)
    elif request.method == 'POST':
    	return Response({"message": "POST method", "data": post})    
    elif request.method == 'PUT':
        return Response({"message": "PUT method", "data": request.data})
    elif request.method == 'DELETE':
        return Response({"message": "DELETE Method", "data": request.data})


@login_required(login_url="home")
@api_view(['POST'])
def FriendRequestHandler(request):
    if request.method == 'POST':
    	return Response({"message": "POST method", "data": post})    

# https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
# https://www.django-rest-framework.org/api-guide/views/
#@login_required(login_url="home")
#@api_view(['GET'])
class PostToUserHandlerView(APIView):

    def get(self, request, format=None):
    	current_user_id = int(self.request.user.id)
    	posts = Post.objects.filter(author_id=current_user_id)
    	return Response(PostSerializer(posts, many=True).data)


# https://stackoverflow.com/questions/19360874/pass-url-argument-to-listview-queryset
#@login_required(login_url="home")
#@api_view(['GET'])
class PostToUserIDHandler(APIView):

    def get(self, request, user_id, format=None):
    	posts = Post.objects.filter(author_id=user_id)
    	return Response(PostSerializer(posts, many=True).data)

@login_required(login_url="home")
@api_view(['POST'])
def FriendQueryHandler(request, user_id):
    if request.method == 'POST':
    	return Response({"message": "POST method", "data": post})    

@login_required(login_url="home")
@api_view(['GET'])
def Friend2FriendHandler(request, user_id1, user_id2):
    if request.method == 'GET':
    	return Response({"message": "GET method", "data": post})    


@login_required(login_url="home")
@api_view(['GET'])
def AuthorProfileHandler(request, user_id):
    if request.method == 'GET':
    	return Response({"message": "GET method", "data": post})    
