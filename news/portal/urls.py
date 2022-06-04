from django.urls import path
from .views import PostAddView

urlpatterns = [
    path('add', PostAddView.as_view(), name='add'),

]