from django.urls import path
from .views import PostAddView, PostListView, PostDetail, post, PostUdateView, PostDeleteView, CommentUdateView, \
    contact #для проверки (удалить)

urlpatterns = [
    path('add', PostAddView.as_view(), name='add'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('user', post, name='post'),
    path('<int:pk>/edit', PostUdateView.as_view(), name='post_create'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/comment', CommentUdateView.as_view(), name='comment_update'),
    path('cont', contact, name='contact'), #для проверки (удалить)

    #ajax
    # path('update_comment_status/<int:pk>/<slug:type>', update_comment_status, name='update_comment_status')

]