import requests, re, os, time, pickle
from lxml import etree
import aiohttp
import asyncio
import js2py
import threading
import queue
from tqdm import tqdm
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

start_url = 'https://manhua.dmzj.com/tags/marvel.shtml'

server = 'https://manhua.dmzj.com'
img_sever = 'https://images.dmzj.com/'
path = 'F:\\pyData\\marvel'
# 线程数量
threadNum = 16
# 提取每一章节url的请求头
headers = {
	'Referer' : 'https://manhua.dmzj.com/tags/marvel.shtml',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400',
}

# 提取每一章节的url和title
def get_url_list(que):
	for url in que:
		r = requests.get(url,headers = headers, verify = False)
		r.encoding = r.apparent_encoding
		s = etree.HTML(r.text)
		comic_name = s.xpath('//span[@class="anim_title_text"]//h1/text()')[0]
		comic_name = re.sub('[\/:*?"<>|]','-', comic_name)
		comic_path = os.path.join(path, comic_name)
		if not os.path.exists(comic_path):
			os.makedirs(comic_path)
		titles = s.xpath('//div[@class="cartoon_online_border"]//a/@title')
		chapter_urls = s.xpath('//div[@class="cartoon_online_border"]//a/@href')
		for i in range(len(titles)):
			titles[i] = re.sub('[\/:*?"<>|]','-', titles[i])
			yield titles[i], server+chapter_urls[i], comic_path

# 提取所有imgurl
def get_imgurls(html):
	a = []
	result = re.findall('eval\(function.*?\);', html, re.S)[0]
	js = 'function get_pages(){%sreturn eval(pages)};' % result
	pages = js2py.eval_js(js)
	for page in pages():
		a.append(img_sever + page)
	return a

# 储存图片
def file_store(path, r):
	with open(path, 'wb') as f:
		f.write(r.content)

# 下载所有图片到本地
def comic_download(chapter_url, html, chapter_path):
	img_urls = get_imgurls(html)
	print('正在下载到%s:' % chapter_path)
	img_headers = {
		'Referer' : chapter_url,
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400',
	}
	for i,img_url in enumerate(img_urls):
		img_name = '%03d.jpg' % i
		img_path = os.path.join(chapter_path, img_name)
		if not os.path.exists(img_path):
			r = requests.get(img_url, headers = img_headers, verify = False)
			file_store(img_path, r)
	print('下载完成！')

# 获取每一章节
async def get_comic(title, chapter_url, comic_path):
	async with aiohttp.ClientSession() as session:
		async with session.request('GET', chapter_url, headers = headers) as resp:
			html = await resp.text()
			chapter_path = os.path.join(comic_path, title)
			if not os.path.exists(chapter_path):
				os.makedirs(chapter_path)
				comic_download(chapter_url, html, chapter_path)

# 获取所有漫画url列表
def get_comicList():
	r = requests.get(start_url, verify = False)
	r.encoding = r.apparent_encoding
	s = etree.HTML(r.text)
	comic_list = s.xpath('//div[@class="pic"]/a/@href')
	a = []
	for comic in comic_list:
		a.append(server + comic)
	return a

class threadDownload(threading.Thread):
	def __init__(self, que):
		threading.Thread.__init__(self)
		self.que = que
	def run(self):
		try:
			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			tasks = [get_comic(title, chapter_url, comic_path) for title, chapter_url, comic_path in self.que]
			loop.run_until_complete(asyncio.wait(tasks))
			loop.close()
		except Exception as e:
			print(e)

def main():
	# urllist = get_comicList()
	urllist = pickle.load(open('F:\\py学习\\test\\comicInfo.p', 'rb'))
	length = len(urllist)
	queList = []
	#将urllist按照线程数目进行切割
	for i in range(threadNum):
		que = []#
		left = i * (length // threadNum)
		if (i+1) * (length // threadNum) < length:
			right = (i+1) * (length // threadNum)
		else:
			right = length
		for url in urllist[left:right]:
			que.append(url)
		queList.append(que)
	threadList = []
	for i in range(threadNum):
		threadList.append(threadDownload(queList[i]))
	for thread in threadList:
		thread.start()
	for thread in threadList:
		thread.join()

if __name__ == '__main__':
	start = time.time()
	main()
	print('总耗时：%.5f秒' % float(time.time()-start))