#import http.server
#import socketserver
import tornado.ioloop
import tornado.web
from os import walk


PORT = 5000

def getItems(path):
	f = []
	for (dirpath, dirnames, filenames) in walk(path):
		f.extend(filenames)
		break
	return f


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		items = getItems("./server_data/")
		self.render("index.html", title="kevtools", items=items)


application = tornado.web.Application([
	(r"/", MainHandler),
])

def run_server():
	application.listen(PORT)
	print("listening on port %d" % PORT)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	run_server()