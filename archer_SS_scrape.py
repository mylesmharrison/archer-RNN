from bs4 import BeautifulSoup
import urllib2

# CREATE SOUP
def soupify(url):

    # Open the request and create the soup
    req = urllib2.Request(url)
    response = urllib2.urlopen(req, timeout = 10.0)
    soup = BeautifulSoup(response.read(), "lxml")
    return soup


# GET SCRIPT AND CLEAN
def get_script(url):
    soup = soupify(url)
    script = soup.findAll("div", {"class":"episode_script"})[0]
    
    # Clean
    for br in script.find_all("br"):
        br.replace_with("\n")
    scripttext = script.text
    scripttext = scripttext.replace('-',' ').replace('\n',' ')
    scripttext = scripttext.strip()

    return scripttext

# GET SCRIPT URLS
def get_episode_urls(showurl):
    
    soup = soupify(showurl)

    # Get the urls and add the base URL to each in the list
    urls = soup.findAll("a", {"class":"season-episode-title"})
    baseurl = 'http://www.springfieldspringfield.co.uk/'
    urls = map(lambda x: baseurl + '/' + x['href'], list(urls))

    return urls

### MAIN

def do_scrape():

	# Scrape the script from each URL and add to a list
	episodes = list()

	# Get the episode list from the main page
	urls = get_episode_urls('http://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=archer')

	for url in urls:
		print url
		episodes.append(get_script(url))  
    
	# Write the output to a file

	f = open('archer_scripts.txt','w')
	for episode in episodes:
		f.write(episode.encode('utf-8'))
    
	f.close()