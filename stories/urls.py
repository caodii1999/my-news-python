from django.urls import path
from . import views
app_name = 'stories'

urlpatterns = [
    path("",views.index,name="index"),
    path("contact.html",views.contact,name="contact.html"),
    path("category.html/<int:pk>/",views.category,name="category.html"),
    path("story.html/<int:pk>/",views.story,name="story.html"),
    path("base.html",views.base,name="base.html"),
    path("search.html",views.search,name="search.html"),
    path("register.html",views.register,name="register.html"),
    path("login.html",views.user_login,name="login.html"),
    path("logout.html",views.user_logout,name="logout.html"),
    path("stories_service.html",views.stories_service,name="stories_service.html"),
    path("subscribe.html",views.subscribe,name="subscribe.html"),
    path("feeds.html",views.read_feeds,name="feeds.html"),

    
]

