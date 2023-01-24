import requests
from bs4 import BeautifulSoup as bs
import os

def get_images(query):
  url = "https://www.google.com/search?q={q}&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq={q}&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"

  q = "+".join(query.lower().split(' '))
  r = requests.get(url.format(q=q), "html.parser")

  soup = bs(r.content)
  # print(soup.prettify())

  images = soup.find_all("img", class_="yWs4tf") 
  
  # return images
  return images[0]['src']

def download_image(target_folder, img_url, file_name):
  file_path = "{}\{}".format(target_folder, file_name)

  try:
    img_data = requests.get(img_url).content

    with open(file_path, 'wb') as handler: 
      handler.write(img_data)

  except Exception as e:
    print("Could not load : " + img_url)
    print(e)

def search_and_download(query, target_path='.\imgs\google'):
  img_urls = get_images(query)
  target_folder = os.path.join(target_path,'_'.join(query.lower().split(' ')))

  if not os.path.exists(target_folder):
    os.makedirs(target_folder)

  for i, img in enumerate(img_urls[0:2]):
    download_image(target_folder, img['src'], str(i) + ".jpg")

# search_and_download("peru")
# get_images("query")