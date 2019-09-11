import requests, re, os, time, pickle
from lxml import etree
import aiohttp, asyncio, js2py, threading, queue
from tqdm import tqdm
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

start_url = 'https://m.mkzhan.com/213945/'
server = 'https://m.mkzhan.com/'
path = 'F:\\pyData\\辉夜大小姐想让我告白'
headers = {
		'Referer': start_url,
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400',
	}
fail_url = []

def file_store(path, r):
	with open(path, 'wb') as f:
		f.write(r.content)

def comic_download(chapter_url, html, chapter_path):
	s = etree.HTML(html)
	img_url_list = s.xpath('//ul[@class="comic-list"]//img/@src')

	for i,img_url in tqdm(enumerate(img_url_list)):
		img_name = '%03d.jpg' % i
		img_path = os.path.join(chapter_path, img_name)
		if not os.path.exists(img_path):
			r = requests.get(img_url, headers = headers, verify = False)
			file_store(img_path, r)

def get_chapter_url(url):
	r = requests.get(url, headers = headers, verify = False)
	r.encoding = r.apparent_encoding
	s = etree.HTML(r.text)
	chapter_urls = s.xpath('//li[@class="chapter-item"]//a/@href')
	titles = s.xpath('//li[@class="chapter-item"]//a/text()')
	for i in range(len(chapter_urls)):
		titles[i] = re.sub('\s|\n|<[^>]+>','', titles[i])
		if titles[i][0] != '第':
			titles[i] = '第%s话' % titles[i]
		yield titles[i], server+chapter_urls[i]

async def get_comic(title, chapter_url):
	global fail_url
	try:
		async with aiohttp.ClientSession() as session:
			async with session.request('GET', chapter_url, headers = headers) as resp:
				html = await resp.text()
				chapter_path = os.path.join(path, title)
				if not os.path.exists(chapter_path):
					os.makedirs(chapter_path)
				comic_download(chapter_url, html, chapter_path)
	except Exception as e:
		print(e)
		fail_url.append[chapter_url]


# 调用方
def main():
	loop = asyncio.get_event_loop()
	tasks = [get_comic(title, chapter_url) for title, chapter_url in get_chapter_url(start_url)]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()

if __name__ == '__main__':
	start = time.time()
	main()
	print('失败url列表：')
	print(fail_url)
	print('总耗时：%.5f秒' % float(time.time()-start))