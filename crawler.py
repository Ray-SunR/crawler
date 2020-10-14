import httplib2
from queue import Queue
import json
from bs4 import BeautifulSoup
import sys

http = httplib2.Http()

queue = Queue()
visited = set()
site_maps = {}

def serialize_sets(obj):
  if isinstance(obj, set):
    return list(obj)
  return obj

def get_links(base_url, url):
  links = []
  assets = []
  status, response = http.request(url)
  soup = BeautifulSoup(response, features="html.parser")
  
  for link in soup.findAll('link'):
    if link.has_attr('href'):
      assets.append(link['href'])

  for script in soup.findAll('script'):
    if script.has_attr('src'):
      assets.append(script['src'])

  for link in soup.findAll('a'):
    if link.has_attr('href'):
      normallized_url = get_normallized_link(base_url, link['href'])
      if normallized_url.startswith(base_url):
        links.append(normallized_url)
  return assets, links

def get_normallized_link(base_url, url):
  return base_url + url if url.startswith('/') else url

def crawl(base_url):
  queue.put(base_url)
  visited.add(base_url)
  while not queue.empty():
    url = queue.get()
    print('visit: ' + url)
    assets, links = get_links(base_url, url)
    for link in links:
      if url not in site_maps:
        site_maps[url] = {
          'assets': assets, 
          'pages': set([link])
        }
      else:
        site_maps[url]['pages'].add(link)
      if link not in visited:
        queue.put(link)
        visited.add(link)
  with open('site_maps', 'wb') as f:
    f.write(json.dumps(site_maps, indent=4, default=serialize_sets).encode('utf-8'))

def main():
  base_url = input('Enter url to crawl\n')
  print('Crawling ' + base_url)
  crawl(base_url)
  print('Crawling completed...')
  while True:
    try:
      url = input('Enter url to query site maps and static assets...\nPress ctrl-c to quit\n')
      if url not in site_maps:
        print(url + ' does not exist in ' + base_url)
      else:
        print('pages: ', list(site_maps[url]['pages']))
        print('assets: ', site_maps[url]['assets'])
    except KeyboardInterrupt:
      print('quiting...')
      sys.exit(1)

if __name__ == '__main__':
  main()
