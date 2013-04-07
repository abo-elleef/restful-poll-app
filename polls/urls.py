from django.conf.urls import patterns, url
from polls import views


urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^new/$',views.new,name='new'),
	url(r'^create/$',views.create,name='create'),
	url(r'^(?P<poll_id>\d+)/$',views.show,name='show'),
	url(r'^(?P<poll_id>\d+)/edit/$',views.edit,name='edit'),
	url(r'^(?P<poll_id>\d+)/update/$',views.update,name='update'),
	url(r'^(?P<poll_id>\d+)/destroy/$',views.destroy,name='destroy'),
	url(r'^(?P<poll_id>\d+)/vote/$',views.vote,name='vote'),
	url(r'^(?P<poll_id>\d+)/add_vote/$',views.add_vote,name='add_vote'),
	)
