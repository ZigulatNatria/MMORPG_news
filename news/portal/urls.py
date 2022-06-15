from django.urls import path
from .views import PostAddView, PostListView, PostDetail, \
    contact #для проверки

urlpatterns = [
    path('add', PostAddView.as_view(), name='add'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('cont', contact, name='contact') #для проверки

]