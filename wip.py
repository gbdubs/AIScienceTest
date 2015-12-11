import urllib2
import json
import os.path

data_root = '/home/u/fall12/gward/Desktop/AI/running/wikipedia/'



def article_found(json_response):
	if "\"missing\":\"\"" in json_response and len(json_response) < 500:
		return False
	return True

def get_content_from_json(json_response):
	page_id_start = json_response.index("\"pageid\":") + 9
	page_id_end = json_response.index(',', page_id_start)
	print page_id_start
	print page_id_end
	page_id = json_response[page_id_start: page_id_end]
	print page_id

	resp = json.loads(json_response)
	return resp["query"]["pages"][page_id]["extract"].encode('utf-8')

def get_wikipedia_article(topic_name):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	topic_name = topic_name.strip('!@#$%^&*()-=[]{}\'\"')
	topic_name = topic_name.replace(' ', '%20')
	url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext=&titles='+topic_name
	infile = opener.open(url)
	page = infile.read()
	if not article_found(page):
		return None
	return get_content_from_json(page)

def process_article(article):
	stop_words = set(["", "a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours  ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"])
  	strip_chars = '().-\'":!.,?![]{}+= '
  	new_words = list()
  	for word in article.split():
  		new_word = word.strip(strip_chars).lower()
  		if new_word not in stop_words:
  			new_words.append(new_word)
  	return new_words

def get_word_list(topic_name):
	expected_path = data_root + topic_name + ".txt"
	if os.path.isfile(expected_path):
		print "FILE FOUND! SKIPPING WIKIPEDIA!"
		f = open(expected_path, 'r')
		return f.read().split(" ")
	else:
		print "FILE NOT FOUND, GOING TO WIKIPEDIA!"
		data_list = process_article(get_wikipedia_article(topic_name))
		data = " ".join(data_list)
		print(data)
		f = open(expected_path, 'w')
		f.write(data)
		return data_list

def main():
	get_word_list("George Lucas")





if __name__ == '__main__':
	main()