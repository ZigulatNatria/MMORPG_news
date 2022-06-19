from django.urls import path
from .views import PostAddView, PostListView, PostDetail, post, PostUdateView, \
    PostDeleteView, CommentDetail, ProtectPostDetail

urlpatterns = [
    path('add', PostAddView.as_view(), name='add'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('user', post, name='post'),
    path('<int:pk>/edit', PostUdateView.as_view(), name='post_create'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment'),
    path('user/<int:pk>', ProtectPostDetail.as_view(), name='post'),


    #ajax
    # path('update_comment_status/<int:pk>/<slug:type>', update_comment_status, name='update_comment_status')

]