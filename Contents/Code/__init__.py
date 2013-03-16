API_KEY = 'rTvtu68O91ctXH9GHJVFlyxUtWjcsnuo'
BASE_URL = 'http://www.theverge.com'
VIDEO_URL = BASE_URL + '/api/v2/videos?api_key=' + API_KEY + '&iphone_client_version=2&page=%d&label=%s'
IMAGE_URL = 'http://cdn0.sbnation.com/api/v2/entries/photos?api_key=' + API_KEY + '&iphone_client_version=2&entry_id=%s&width=640&format=png' 

####################################################################################################
def Start():

	ObjectContainer.title1 = "The Verge"
	HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler('/video/theverge', "The Verge")
def MainMenu():

	oc = ObjectContainer()

	oc.add(DirectoryObject(
			key = Callback(ListPodcast, podcast='all'),
			title = 'Latest Videos'
		))

	oc.add(DirectoryObject(
			key = Callback(ListPodcast, podcast='On The Verge'),
			title = 'On The Verge (Full Episodes)'
		))

	# for podcast in HTML.ElementFromURL(BASE_URL).xpath('//div[@id="show-dropdown"]/a/h2'):
	# 	oc.add(DirectoryObject(
	# 		key = Callback(ListPodcast, podcast=podcast.text),
	# 		title = podcast.text
	# 	))

	return oc

####################################################################################################
@route('/video/theverge/listpodcast/{podcast}/{page}', podcast=str, page=int)
def ListPodcast(podcast='all', page=1):
	if podcast == 'all':
		pc_name = ''
	else:
		pc_name = podcast

	oc = ObjectContainer()
	
	res = JSON.ObjectFromURL(VIDEO_URL % (page, String.Quote(pc_name)))
	for video in res['entries']:
		if video['mp4_link']:
			oc.add(VideoClipObject(
					url = video['url'],
					title = video['title'],
					thumb = Resource.ContentsOfURLWithFallback(url=[IMAGE_URL % video['id']])
				))

	if int(res['total_pages']) > int(res['current_page']):
		oc.add(NextPageObject(key=Callback(ListPodcast, podcast=podcast, page=page+1), title="More Videos..."))
	return oc