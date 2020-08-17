from django.urls import path

from .views import (
    home_view, 
    tweet_action_view, 
    tweet_detail_view, 
    tweet_list_view, 
    tweet_create_view,
    tweet_delete_view
)

'''
Base ENDPOINT is /api/tweets/
'''
urlpatterns = [
    path('', tweet_list_view),  #/api/tweets/
    path('action/',tweet_action_view),  #api/tweets/action/
    path('create/', tweet_create_view), #/api/tweets/create/
    path('<int:tweet_id>/', tweet_detail_view), #/api/tweets/24/
    path('<int:tweet_id>/delete/', tweet_delete_view), #/api/tweets/24/delete/
]