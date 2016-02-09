from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django import forms
import praw
import json
import logging

logger = logging.getLogger('django')

class SearchForm(forms.Form):
	search = forms.CharField(label='',max_length=100, required=False,)
	

def index(request):
	logger.debug('django POST has been hit.')
	subreddit_list = []
	if request.method == 'POST':
		form = SearchForm(request.POST, auto_id='search')
		if(form.is_valid()):
			subreddit_list = sub_search(form.cleaned_data['search'])
	else:
		logger.debug(request)
		form = SearchForm(auto_id='search')
		subreddit_list = ""
	return render_to_response("sockettest/base.html",
	{},
	context_instance = RequestContext(request))
	
def ajax(request):
	logger.debug('Printing ajax request: %r' % request.POST)
	tile_list = []
	if request.method == 'POST':
		subs = request.POST['subs']
		tile_list = sub_search(subs)
		return HttpResponse(json.dumps(tile_list), content_type="application/json")
		

def sub_search(request):
	logger.debug("Sub search has been hit with this request: %r" % request)
	tile_list = []
	reddit_tile = {}
	submission_list = []
	user = get_user()
	if(request):
		subs_list = request
		subs_list = subs_list.split('+')
		for subs in subs_list:		
			subreddit = user.get_subreddit(subs)
			title = subs.encode('utf8')
			#submission_list.append("--- " + title + " ---")
			reddit_tile['title'] = title
			for submission in subreddit.get_hot(limit = 5):
				message = "Title: " + submission.title.encode('utf8')
				message += " Score: " + str(submission.score)
				message += " "
				submission_list.append(message)
				reddit_tile['submission'] = submission_list
			submission_list = []
			tile_list.append(reddit_tile)
			reddit_tile = {}
	return tile_list


def get_user():
	user = praw.Reddit(user_agent = 'PyMan v1')
	return user
