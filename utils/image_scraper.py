from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
import os

driver_path = "C:\\Users\\Javier\\Desktop\\chromedriver_win32\\chromedriver.exe"

def get_images(query, wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?q={q}&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq={q}&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"

	q = "+".join(query.lower().split(' '))

	wd.get(url.format(q=q))

	img_urls = set()
	skips = 0

	while len(img_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(img_urls) + skips : max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in img_urls:
					max_images += 1
					skips += 1
					break

				elif image.get_attribute('src') and 'http' in image.get_attribute('src'):
					img_urls.add(image.get_attribute('src'))
					print(f"Found {len(img_urls)} {image.get_attribute('src')}")

				else:
					max_images += 1
					skips += 1

	# return img_urls
	return list(img_urls)[0]

def download_image(target_folder, img_url, file_name):
	try:
		image_content = requests.get(img_url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file).convert('RGB')
		file_path = "{}\{}".format(target_folder, file_name)

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

def search_and_download(query,driver_path=driver_path,target_path='.\imgs\chrome', max_images=2):

	with webdriver.Chrome() as wd:
		img_urls = get_images(query, wd, delay=1, max_images=max_images)

	target_folder = os.path.join(target_path,'_'.join(query.lower().split(' ')))

	if not os.path.exists(target_folder):
		os.makedirs(target_folder)

	for i, img_url in enumerate(img_urls):
		download_image(target_folder, img_url, str(i) + ".jpg")
	
# search_and_download("peru")
# get_images("peru")