import http.server
import socketserver


PORT = 5000

class HTMLPrinter:
	""" Helps with the printing of HTML pages """

	_fout = None

	_indent_level = 0

	def __init__(self, file_path):
		self._fout = open(file_path, 'w')

	def print_header(self):
		self._fout.write(
			"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\""+\
			"\"http://www.w3.org/TR/html4/loose.dtd\">\n\n")
		self._indent_level += 1
		return self

	def write(self, str):
		self._fout.write('\t' * self._indent_level)
		self._fout.write(str + '\n')
		return self

	def indent(self):
		self._indent_level += 1
		return self

	def unindent(self):
		self._indent_level -= 1
		return self

	def close(self):
		self._fout.close()



printer = HTMLPrinter('index.html')

printer.print_header()
printer.write("<html>").indent()
printer.write("<head>").indent()
printer.write("<title>kevtools</title>").unindent()
printer.write("</head>")
printer.write("<body>").indent()
printer.write("<button>Test Button</button>").unindent()
printer.write("</body>").unindent()
printer.write("</html>")

printer.close()

handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), handler)

print("serving at port", PORT)
httpd.serve_forever()