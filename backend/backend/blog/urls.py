
from django.urls import path
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,LikeView,DisLikeView,BlogHome
from . import views
urlpatterns = [
    path('homepage/',BlogHome,name='homepage'),
    path('', BlogHome, name='homepage'),
    path('messageboard/', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('like/<int:pk>/',LikeView,name='like_post'),
    path('Dislike/<int:pk>/', DisLikeView, name='Dislike_post'),

]
 
