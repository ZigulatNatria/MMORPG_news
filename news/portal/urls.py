from django.urls import path
from .views import PostAddView, PostListView, PostDetail

urlpatterns = [
    path('add', PostAddView.as_view(), name='add'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),

]