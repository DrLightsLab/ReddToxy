from django.conf.urls import url

from sockettest.views import reddit

urlpatterns = [
	url(r'^$', reddit.index, name='index'),
	url(r'^/reddit_ajax/', reddit.ajax, name='redditajax'),
]
