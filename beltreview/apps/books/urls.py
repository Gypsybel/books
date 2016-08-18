from django.conf.urls import url
from . import views
from views import index, bookreview 

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),        
    url(r'^addbook$', views.addbook),
    url(r'^bookhome$', views.bookhome),
    url(r'^bookreview/(?P<id>\d+)$', views.bookreview),
    url(r'^user/(?P<id>\d+)$', views.user), 
    url(r'^add$', views.add),
    url(r'^addreview/(?P<id>\d+)$', views.addreview), 
    url(r'^remreview/(?P<rid>\d+)/(?P<bid>\d+)$', views.remreview),  
]