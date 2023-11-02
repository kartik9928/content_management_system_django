from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from app1.models import CustomUser, PostData, PostComments
from app1.serialization import UserSerialize, PostSerialize, CommentSerialize, CustomPostUserSerializer, APIsix, APIsix2, GetAuthorBlogsSerializer, CustomAuthorSearch
from django.contrib.auth.hashers import check_password
from datetime import datetime
from django.db.models import Q, Count
from django.core import serializers


RESET="\[\033[0m\]"         # Text Reset
BLK="\[\033[0;30m\]"        # Black
RED="\[\033[0;31m\]"        # Red
GRN="\[\033[0;32m\]"        # Green
YELLOW="\[\033[0;33m\]"     # Yellow
BLUE="\[\033[0;34m\]"       # Blue
PURP="\[\033[0;35m\]"       # Purple
CYN="\[\033[0;36m\]"        # Cyan
WHT ="\[\033[0;37m\]"       # White

def index(request):
    data = PostData.objects.select_related('author_id').values('title', 'content', 'author_id__last_name', 'author_id__first_name')
    json_data = PostSerialize(data, many=True)
    # json_data = serializers.serialize('json', data)
    print(json_data)
    return HttpResponse("hello")

@api_view(['POST'])
@permission_classes([AllowAny])
def UserCreation(request):
    check = CustomUser.objects.filter(email = request.data['email'])
    if check.count() > 0:
        return Response({'emailAvailable':True})
    # choise = "Subscriber" if request.data['role'] == 3 else ("Author" if request.data['role'] == 2 else "Editor")
    insertData = CustomUser.objects.create_user(
        username= request.data['username'],
        first_name= request.data['first_name'],
        last_name= request.data['last_name'],
        email= request.data['email'],
        role= "Subscriber",
        password= request.data['password'])
    token, created = Token.objects.get_or_create(user=insertData)
    # print(GRN + f'your token key {token.key} and token created {created}' + RESET)
    return Response({'success':True,'token':token.key})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def BlogCreations(request):
    if request.user.is_authenticated:
        FK = CustomUser.objects.get(id=request.user.id)
        if PostData.objects.filter(author_id = request.user.id).count() == 0:
            CustomUser.objects.filter(id = 1 ).update(role = "Author")
        print(RED + f"============================================== this is content :: {request.data['content']}" + RESET)
        data = PostData(
            title = request.data['title'],
            content = request.data['content'],
            author_id = FK,
            published = request.data['published'],
            published_on = datetime.now().date(),
            tags = request.data['tags']
        ).save()
        # data.full_clean()
        return Response({'authentication':True})
    else:
        return Response({'authentication':False,'message':'User is not authenticated'})

@api_view(['POST'])
@permission_classes([AllowAny])
def LoginUser(request):
    login = CustomUser.objects.get(email= request.data['email'])
    if login is not None:
        loginPss = check_password(request.data['password'] , login.password)
        if loginPss:
            token, created = Token.objects.get_or_create(user=login)
            return Response({'login':True,'token':token.key})
    return Response({'login':False})

@api_view(['GET'])
@permission_classes([AllowAny])
def getBlogs(request):
    # data = PostData.objects.all().order_by('-published_on')
    data = PostData.objects.select_related('author_id').values('id', 'title', 'content', 'author_id__last_name', 'author_id__first_name', 'author_id__id')
    jsdata = CustomPostUserSerializer(data, many=True)
    return Response({'authenticated':True, "data":jsdata.data})

@api_view(['POST'])
@permission_classes([AllowAny])
def TagSearch(request):
    toFind = request.data['search']
    data = PostData.objects.filter(Q(tags__icontains=toFind))
    if data.count() != 0:
        jsdata = PostSerialize(data, many=True)
        return Response({"found":True,"isPost":True,"data":jsdata.data})
    data = CustomUser.objects.filter(Q(first_name = toFind) | Q(last_name = toFind), Q(role = "Author")).annotate(TotalBlogs=Count('postdata')).values('id', 'first_name', 'last_name', 'TotalBlogs')
    if data.count() != 0:
        jsdata = CustomAuthorSearch(data, many=True)
        return Response({"found":True,"isAuther":True,"data":jsdata.data})
    return Response({"found":False,"Message":"No Data Found"})

# API_six
@api_view(['POST'])
@permission_classes([AllowAny])
def AutherBlog(request):
    AutherID = request.data['AutherID']
    # Blogs
    Pdata = PostData.objects.filter(author_id = AutherID)
    jsPdata = APIsix2(Pdata, many=True)
    # Auther
    Adata = CustomUser.objects.get(id = AutherID)
    jsAdata = APIsix(Adata, many=False)
    return Response({"AutherData":True,"AutherInfo":jsAdata.data,"autherPost":jsPdata.data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postBlogComment(request):
    if request.user.is_authenticated:
        myid = request.user.id
        postid = request.data['postId']
        myFK = CustomUser.objects.get(id=myid)
        postFK = PostData.objects.get(id=postid)
        data = PostComments(
            post_id = postFK,
            author_id_sub = myFK,
            content = request.data['content'],
            DataTime = datetime.now(),
            seen = False
        ).save()
    return Response({"commented":True})

@api_view(['POST'])
@permission_classes([AllowAny])
def GetBlogComment(request):
    blogId = PostData.objects.get(id = request.data['blogID'])
    commentData = PostComments.objects.filter(post_id = blogId.id)
    JScommentData = CommentSerialize(commentData, many=True)
    return Response({'data':JScommentData.data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def GetAuthorBlogs(request):
    id = request.user.id
    data = PostData.objects.filter(author_id = id)
    datajs = GetAuthorBlogsSerializer(data, many=True)
    author = CustomUser.objects.get(id = id)
    authorJS = APIsix(author , many=False)
    return Response({"data":datajs.data, "author":authorJS.data})

