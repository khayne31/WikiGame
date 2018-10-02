from bs4 import BeautifulSoup
import requests
from googlesearch import search
from collections import Counter
from random import randint
import time
import sys
import webbrowser


def dups(l, value):
	for item in l:
		if value == item:
			return True
	return False

def zip(list_of_strings):
	zipString = ""
	for string in list_of_strings:
		zipString += string + " "
	return zipString[0:-1]

punctuation = [",",":",";", "''","?", ".", "(", ")", "/",  ]
previousPages = ["Main_Page"]


def keywords(query, num_of_requests):
	#builds the url to search for the given query with the given amount of responses
	http = "https://www.google.com/search?q="
	for string in query.split():
		if http[-1] == "=":
			http += string
		else:
			http += "+"+string
	http += "&num="+str(num_of_requests) 

	#requests the given url, html parses the webpage, and returns the elements within the span braces which should be the descriptions of the links
	google = requests.get(http)
	content = google.content
	soup = BeautifulSoup(content, 'html.parser')
	results = soup.find_all('span')

	print(google.status_code)
 	#creates a empty list and appends the text from within the span, encoded in "utf-8", to the list
	descriptions = []
	for item in results:
		descriptions.append(str(str(item.get_text()).encode("utf-8"))[1:])

	#cleans up the data removing "..." and quotes
	descriptions = [x[1:-1].replace("...", "") for x in descriptions if x != "''"]

	new = []
	#removes any strings beginning with \t
	for item in descriptions:
		#turns all strings with an \x in it to a question mark
		new.append([x if r'\x' not in x else "?"for x in item.split()])

	individualWords = []
	for item in new:
		for word in item:
			if r"\n" in word :
				individualWords.append(word.replace(r"\n", ""))
			elif word != "?" and len(word) > 3:
				individualWords.append(word)

	word_count = Counter(individualWords).most_common(len(individualWords))
	#print(word_count)
	return word_count
	#return(individualWords)


#returns a list where each element is of the form (link, title of the link)
def get_wiki_links(topic):
	http = 'https://en.wikipedia.org/wiki/'+topic
	page = requests.get(http)
	#print(http)
	contents = page.content
	soup = BeautifulSoup(contents, 'html.parser')
	links = soup.find_all('a')
	new_links = []
	#gets the links which will direct to a wiki page and add them to a new list
	for item in links:
		if(str(item.get('href'))[0:5] == "/wiki" and r"\x" not in str(str(item.get('title')).encode("utf-8"))) and ":" not in str(item.get('href')):
			if not dups(new_links, [str(item.get('href')), str(str(item.get('title')).encode("utf-8"))[1:-1], 0]):
				new_links.append([str(item.get('href')), str(str(item.get('title')).encode("utf-8"))[1:-1], 0])
	return new_links
query = "paris"
#print(get_wiki_links(query))

def replace_in_string(string, list_of_items_to_remove):
	returnstring = string
	for item in list_of_items_to_remove:
		returnstring.replace(item, "")
	return returnstring




def return_new_link(starting_page, keywordslist, target_page):
	links  = get_wiki_links(starting_page)
	perfect_hit = ""

	#for some reason there is an apostrophe before the string which for some reason wont be removed so well just test all chars but the first one
	for item in links:
		for word in keywordslist:
			if item[1][1:].lower() == target_page.lower():
				perfect_hit = item[0]
			elif word[0] in item[1]:
				item[2] += word[1]

	links = [(x[2],x[0], x[1]) for x in links if perfect_hit == "" and x[0][6:] not in previousPages]
	#[numer_of_hits, link, title of link]
	links = [x for x in sorted(links, reverse = True)]
	#print(links)
	if perfect_hit != "":
		return perfect_hit
	elif  links[0][0]>1:
		return links[0][1]
	elif links[0][0] == 1:
		temp = [x[1] for x in links if x[0] != 0]
		return temp[randint(0,len(temp)-1)]
	elif  links[0][0] == 0:
		return links[randint(0, len(links)-1)][1]



def wiki_links(starting_page, ending_page):
	f = open("wiki.txt", "a")
	start = starting_page
	end = ending_page
	keywordslist = keywords(end, 100)
	desination_reached = False
	iterations = 0
	while(not desination_reached and iterations < 500000):
		temp = return_new_link(start, keywordslist, end)
		previousPages.append(start)
		#print(previousPages)
		start = temp[6:]
		print(start)
		sys.stdout.flush()
		iterations += 1
		desination_reached = ending_page.lower() ==  start.replace("_", " ").partition("#")[0].lower()
		#time.sleep(50)
	return (start,iterations)


#print("chicken#awesome".partition("#")[0])

#print(return_new_link("elmo", "Saddam Hussein"))
#print(wiki_links("kentukcy", "ostrich"))
result = wiki_links("evil", "triple h")
webbrowser.open("https://en.wikipedia.org/wiki/"+result[0])
print(result[1])
#print(keywords("hitler", 30))
