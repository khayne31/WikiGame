from bs4 import BeautifulSoup
import requests
from googlesearch import search
from collections import Counter
from random import randint
import time
import sys


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
    

		#print(str(item.get('href')) +",\t"+ str(item.get('title')))

#goes to one of the new links and creates a new BeautifulSoup obj
"""page2 = requests.get("https://en.wikipedia.org"+str(fresh_links[3][0]))
contents2 = page2.content
soup2 = BeautifulSoup(contents2, 'html.parser')
links2 = soup2.find_all('p')"""
#for item in links2:
	#print(item)


"""query = "Saddam Hussein"
search = search(query, tld = "com", lang = "en", num = 100, stop = 1, pause = 2 )
reference_links = []
for item in search:
	if "wikipedia" not in str(item):
		reference_links.append(item)
		#print(item)

gsearchp1 = requests.get(str(reference_links[1]))
print(str(reference_links[1]))
gcontents = gsearchp1.content
soup3 = BeautifulSoup(gcontents, 'html.parser')

f = open("gsearch.txt", 'w')

text = soup3.find_all('p')
for item in text:
	f.write(str(item.get_text())+ "\n")

f.close()"""



#print(individualWords[13].replace(r"\n", ""))



#word_count = [x for  x in word_count if x[]
#print(str(links3).encode("utf-8"))

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




def return_new_link(starting_page, target_page):
	links  = get_wiki_links(starting_page)
	keywordslist = keywords(target_page, 30)
	perfect_hit = ""

	#for some reason there is an apostrophe before the string which for some reason wont be removed so well just test all chars but the first one
	for item in links:
		for word in keywordslist:
			if item[1][1:].lower() == target_page.lower():
				perfect_hit = item[0]
			elif word[0] in item[1]:
				item[2] += word[1]

	links = [(x[2],x[0], x[1]) for x in links if perfect_hit == ""]
	links = [x for x in sorted(links, reverse = True)]
	#print(links)
	if perfect_hit != "":
		return perfect_hit
	elif  links[0][0]>1:
		return links[0][1]
	elif links[0][0] == 1:
		temp = [x[1] for x in links if x[0] != 0]
		return temp[randint(0,len(temp))]
	#TODO: make a test case when the leading one if equal to one
	elif  links[0][0] == 0:
		return links[randint(0, len(links))][0]



def wiki_links(starting_page, ending_page):
	f = open("wiki.txt", "a")
	start = starting_page
	end = ending_page
	desination_reached = False
	iterations = 0
	while(not desination_reached and iterations < 10):
		temp = return_new_link(start, end)
		start = temp[6:]
		print(start)
		sys.stdout.flush()
		iterations += 1
		desination_reached = ending_page ==  start.replace("_", " ")


wiki_links("georgia", "chicken")
#print(return_new_link("elmo", "Saddam Hussein"))