import urllib
import json

response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft")
tweets_dict = json.load(response)

results_list = tweets_dict['results']

for result_dict in results_list:
	for key in result_dict:
		if key == 'text':
			print 'tweet:', result_dict[key]
