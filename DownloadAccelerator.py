import argparse
import requests
import threading


class DownloadRangeThread(threading.Thread):
    def __init__(self, url, lowerBound, upperBound):
        threading.Thread.__init__(self)
        self.url = url
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def run(self):
		byteRange = "bytes=" + str(self.lowerBound) + "-" + str(self.upperBound)
		print byteRange
		headers = {"Range" : byteRange, "Cache-Control" : "no-cache, no-store, must-revalidate"}
		r = requests.get(self.url, headers = headers)
		#r = requests.get(url)
		self.content = r.content
		print("--------------- -- -- -- -- -- -- -- - - - ---")

class DownloadAccelerator:
	def __init__(self, threads):
		args = self.parse_args()
		self.stringValues = [None] * args.t
		print(self.stringValues)
		self.download_file(args.url, args.t)

	def parse_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-t', type = int, help='Number of threads', default=10 )
		parser.add_argument("url", help="url")
		return parser.parse_args()

	def download_file(self, url, threads):
		r = requests.head(url)
		length = int(r.headers["content-length"])
		print("length: " + str(length))

		threadList = []
		increment = length//threads

		lowerBound = 0;
		upperBound = 0;
		for i in range(0, threads):
			if ( i != threads - 1):
				upperBound = lowerBound + increment - 1;
			else:
				upperBound = length;

			print(i,": ", lowerBound, upperBound)

			#download chunk
			threadList.append(DownloadRangeThread(url, lowerBound, upperBound))

			lowerBound = upperBound + 1

		for t in threadList:
			t.start()


		for t in threadList:
			t.join()

		filename = "index.html";
		if(url.endswith("\\")):
			filename = "index.html"
		else:
			words = url.split("\\")
			filename = words[-1]

		with open(filename, 'wb') as f:
			f.seek(0)
			f.truncate()
			for t in threadList:
				f.write(t.content)



		print('done')	

da = DownloadAccelerator(10)