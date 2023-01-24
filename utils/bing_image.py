from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import os
import json

def get_images(query):

  def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
      urllib.request.Request(url,headers=header)),
      'html.parser')

  query='+'.join(query.split())
  url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

  header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
  soup = get_soup(url,header)

  img_urls=[]

  for a in soup.find_all("a",{"class":"iusc"}):
    m = json.loads(a["m"])
    murl = m["murl"]
    turl = m["turl"]

    img_name = urllib.parse.urlsplit(murl).path.split("/")[-1]

    img_urls.append((img_name, turl, murl))
  
  # return img_urls
  print(img_urls[0][2])
  return img_urls[0][2]

def download_image(target_folder, img_url, file_name):
  file_path = "{}\{}".format(target_folder, file_name)

  try:
    img_data = urllib.request.urlopen(img_url).read()

    with open(file_path, 'wb') as handler: 
      handler.write(img_data)

  except Exception as e:
    print("Could not load : " + img_url)
    print(e)
  
def search_and_download(query, target_path='.\imgs\\bing'):
  img_urls = get_images(query)
  target_folder = os.path.join(target_path,'_'.join(query.lower().split(' ')))

  if not os.path.exists(target_folder):
    os.makedirs(target_folder)

  for i, (image_name, turl, murl) in enumerate(img_urls[0:2]):
    download_image(target_folder, murl, str(i) + ".jpg")

# search_and_download("query")
# get_images("paolo guerrero")