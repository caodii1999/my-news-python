# rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import StorySerializer, CategorySerializer

from django.shortcuts import render
from django.http import HttpResponse
import json
from . import models
import datetime
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from mynews.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

import feedparser

now = datetime.datetime.now()
latest = models.Story.objects.latest('pk')
search_str = ''
newest_4 = models.Story.objects.order_by("-public_day")[0:4]

# Create your views here.
def search(request):
    global search_str
    stories = []
    if request.method == "GET":
        if request.GET.get('name'):
            search_str = request.GET.get('name')
        else:
            search_str = ''
        if search_str != '':
            stories = models.Story.objects.filter(Q(name__contains=search_str)|Q(content__contains=search_str)).order_by("-public_day")
    for story in stories:
        story.content = re.sub('<[^<]+?>', '', story.content)
    numbers = len(stories)
    return render(request,"stories/search.html",{'today':now,'latest':latest,'stories':stories,'newest_4':newest_4,'numbers':numbers,'search_str':search_str})

def index(request):
    story_list = models.Story.objects.order_by("-public_day")
    newest = story_list[0]
    next_4_newest = story_list[1:5]

    young_children = models.Story.objects.filter(category = 1).order_by("-public_day")
    older_children = models.Story.objects.filter(category = 2).order_by("-public_day")

    last_visit = request.session.get('last_visit',False)
    request.session['last_visit'] =  now.strftime('%B %d, %Y %I:%M %p')

    value = 1
    if request.COOKIES.get('visits'):
        value = int(request.COOKIES.get('visits'))
    response = render(request,"stories/index.html",{'today':now,'stories':story_list,'newest':newest, 'next_4_newest':next_4_newest,'young':young_children, 'older':older_children,'latest':latest, 'visits':value, 'last_visit':last_visit})
    
    # if request.COOKIES.get('visits'):
    if value != 1:
        response.set_cookie('visits', value+1)
    else:
        response.set_cookie('visits', value)
    return response

    # return render(request,"stories/index.html",{'today':now,'stories':story_list,'newest':newest, 'next_4_newest':next_4_newest,'young':young_children, 'older':older_children,'latest':latest})

def category(request, pk):
    story_list = models.Story.objects.filter(category=pk)
    for story in story_list:
        story.content = re.sub('<[^<]+?>', '', story.content)

    page = request.GET.get('page',1) # trang bat dau
    paginator = Paginator(story_list,4) # so story/trang

    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)


    newest = models.Story.objects.filter(category=pk).order_by("-public_day")[0:4]
    
    return render(request,"stories/category.html", {'today':now,'stories':stories, 'newest':newest, 'pk':pk, 'latest':latest})

def story(request, pk):
    story_select = models.Story.objects.get(pk = pk)
    stories = models.Story.objects.filter(category=story_select.category).order_by("-public_day")
    newest = models.Story.objects.order_by("-public_day")[0:4]
    return render(request,"stories/story.html",{'today':now,'story':story_select,'stories':stories,'newest':newest, 'latest':latest})

def contact(request):
    result = ''
    form = forms.FormContact()

    return render(request,"stories/contact.html",{'today':now,'newest_4':newest_4,'latest':latest,
    'result':result,'form':form})    

def base(request):
   
    return render(request,"base.html",{'today':now,'newest_4':newest_4,'latest':latest})    

def register(request):
    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)
        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()

            registered = True
        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error('confirm',' The Password do not match')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    last_visit = request.session.get('last_visit', False)
    username = request.session.get('username', 0)

    return render(request,"stories/register.html",{'today':now,'user_form':form_user,'profile_form':form_por,'last_visit':last_visit,'latest':latest,'registered':registered,'username':username}) 

def user_login(request):
    last_visit = request.session.get('last_visit', False)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            result = "Hello " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request,"stories/login.html",{'today':now,'last_visit':last_visit,'latest':latest,'login_result':result, 'username':username})
        else:
            login_result = "Username or password is incorrect !"
            return render(request,"stories/login.html",{'today':now,'last_visit':last_visit,'latest':latest,'login_result':result})
    else:
        return render(request,"stories/login.html",{'today':now,'last_visit':last_visit,'latest':latest})


def user_logout(request):
    last_visit = request.session.get('last_visit', False)

    return render(request,"stories/logout.html",{'today':now,'last_visit':last_visit,'latest':latest}) 

def stories_service(request):
    stories = models.Story.objects.order_by("-public_day")
    result_list = list(stories.values('category','name','author','url','public_day','image','content'))
    return HttpResponse(json.dumps(result_list, indent=4, sort_keys=True, default=str).encode('utf8'))


class StoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed stories (or edited)
    """
    queryset = models.Story.objects.all().order_by('-public_day')    
    serializer_class = StorySerializer
    # Cấp quyền cho người dùng
    # permission_classes = [permissions.IsAdminUser] # đọc/ ghi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # chỉ đọc
    

def subscribe(request):
    last_visit = request.session.get('last_visit', False)
    username = request.session.get('username', 0)
    if request.method == 'POST':
        email_address = request.POST.get("email")
        subject = 'Welcome to Stories for Children Website'
        message = 'Hope you are enjoying your stories !'
        recepient = str(email_address)
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
        result = "Our email was sent to your mail box . Thank you. "

        return render(request,"base.html",{'today':now,'newest_4':newest_4,'latest':latest,'result':result,'last_visit':last_visit,'username':username})    

    return render(request,"base.html",{'today':now,'newest_4':newest_4,'latest':latest,'last_visit':last_visit,'username':username}) 


def read_feeds(request):
    news_feed = feedparser.parse("http://feeds.feedburner.com/bedtimeshortstories/LYCF")
    entry = news_feed.entries
    # print(entry)

    last_visit = request.session.get('last_visit', False)
    username = request.session.get('username', 0)

    return render(request,"stories/feeds.html",{'today':now,'newest_4':newest_4,'latest':latest,'last_visit':last_visit,'username':username, 'feeds':entry}) 