from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^person/$', views.PersonView.as_view(), name='person'),
    url(r'^search/$', views.SearchView.as_view(), name='search')
]