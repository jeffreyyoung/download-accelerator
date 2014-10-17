import argparse
import requests
import threading
from pudb import set_trace;  #debugging



class DownloadAccelerator:
	def __init__(self, threads):
		args = self.parse_args()
		self.download_file(args.url, args.t)

	def parse_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-t', type = int, help='Number of threads', default=10 )
		parser.add_argument("url", help="url")
		return parser.parse_args()

	def download_range(self, url, lowerBound, upperBound, byteList):
		byteRange = "bytes=" + str(lowerBound) + "-" + str(upperBound)
		print byteRange
		headers = {"Range" : byteRange, "Cache-Control" : "no-cache, no-store, must-revalidate"}
		r = requests.get(url, headers = headers)
		#r = requests.get(url)

		with threading.Lock():
			byteList.append(r.text)
			print(r.text)
		print("--------------- -- -- -- -- -- -- -- - - - ---")

	def download_file(self, url, threads):
		r = requests.head(url)
		length = int(r.headers["content-length"])
		print("length: " + str(length))
		byteList = []
		threadList = []
		increment = length/threads
		#increment = 10

		lowerBound = 0;
		#set_trace()
		for i in range(0, threads):
			upperBound = lowerBound + increment
			print(lowerBound, upperBound)
			t = threading.Thread(target=self.download_range, args = (url, lowerBound, upperBound, byteList))
			t.daemon = True
			lowerBound = lowerBound + increment + 1
			threadList.append(t)

		for t in threadList:
			t.start()


		for t in threadList:
			t.join()

		with open('text.txt', 'wb') as f:
			f.seek(0)
			f.truncate()
			for s in byteList:
				f.write(s)

		print('done')	

da = DownloadAccelerator(10)
