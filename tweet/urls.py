from django.urls import path 
from .import views
urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.tweet_list,name='tweet_list'),
    path('create/',views.tweet_create,name='tweet_create'),
    path('<int:tweet_id>/edit/',views.tweet_edit,name='tweet_edit'), #for need id 
    path('<int:tweet_id>/delete/',views.tweet_delete,name='tweet_delete'),
    path('register/',views.register,name='register'),
    path('profile/', views.profile, name='profile'),
    path('tweet_like/<int:pk>',views.tweet_like,name="tweet_like"),
    path('search/', views.search_results, name='search_results'),

]
