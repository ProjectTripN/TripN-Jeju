from django.conf.urls import url
from django.urls import path

from chat import views

urlpatterns = [
    path(r'uploader', views.uploaderDB),
    path(r'with', views.with_who),
    path(r'where', views.where_air),
    path(r'chat', views.chat),

]