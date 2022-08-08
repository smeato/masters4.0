from django.urls import path
from . import views 
from scrapbook.views import ScrapbookView

app_name = 'scrapbook'
urlpatterns = [
    path('', views.index, name='index'),
    path('view/<str:username>/', views.ScrapbookView.as_view(), name='scrapbook_view'),
    path('random-page/<str:username>/', views.random_page, name='random_page'),
    path('create-page/<str:username>', views.PageCreateView.as_view(), name='create_page'),
    path('complete-page/<int:page_pk>', views.complete_page, name='complete_page'),
    path('complete-page/song-search/', views.song_search, name='song_search'),
    path('complete-page/song-save/', views.song_save, name='song_save'),
    path('complete-page/youtube-search/', views.youtube_search, name='youtube_search'),
    #path('create-gallery/<int:page_pk>/', views.create_gallery, name='create_gallery'),
    path('view/<int:page_pk>', views.page_view, name='page_view'), 
    path('view/page/add-note/', views.add_note, name='add_note'),
    path('view/page/<int:page_pk>/notes', views.view_notes, name='view_notes'),
    path('activities/', views.activities, name='activities'),
    path('help/', views.help_page, name='help'),
    path('login', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register', views.register, name='register'),
    path('account-help', views.account_recovery, name='account_recovery'),
    path('access-denied', views.no_access, name='no_access'),
    path('ajax', views.AjaxTest.as_view(), name='ajax_test'),
]