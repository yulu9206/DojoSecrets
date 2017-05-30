from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^logout$', views.logout),
  url(r'^secrets$', views.secrets),
  url(r'^like/(?P<secret_id>\d+)/(?P<fromurl>\w+)$', views.like),
  url(r'^delete/(?P<secret_id>\d+)/(?P<fromurl>\w+)$', views.delete),
  url(r'^post$', views.post),
  url(r'^secrets/$', views.pop_secrets),
]