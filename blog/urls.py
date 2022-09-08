from django.urls import path
from . import views
urlpatterns = [

    path('', views.post_list, name='post_list'),
    #path('upload/', views.post_list, name='post_list'),
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
    path('new/', views.post_new, name='post_new'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/edit/', views.post_edit, name="post_edit"),
    path('<slug:slug>/delete/', views.DeletePostView.as_view(), name='post_delete'),

]
