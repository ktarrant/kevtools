#!/usr/bin/env python

import os
import sys
import urllib.request
import time

def getInfoString(bytes):
	units = ("B", "K", "M", "G", "T", "P")
	unitChoice = 0
	bytes_f = float(bytes)
	while bytes_f > 1024:
		bytes_f = bytes_f / 1024.0
		unitChoice = unitChoice + 1
	if unitChoice >= len(units):
		return "%.2f ?B" % bytes_f
	else:
		return "%.2f %sB" % (bytes_f, units[unitChoice])

def _downloadData(HTTPObject, saveFile, printStatus=True):
	fileObject = open(saveFile, 'wb')
	content_header = HTTPObject.getheader("Content-length")
	if (content_header is None):
		if (printStatus):
			print("Unable to retrieve content header.")
		return False
	file_size = int(HTTPObject.getheader("Content-length"))
	if (printStatus):
		sys.stdout.write("Downloading \"%s\" ... (%s)\n" \
			% (saveFile, getInfoString(file_size)))	
	file_size_dl = 0
	block_sz = 8192
	dotThresh = file_size / 100
	curDot = 1
	if (printStatus):
		sys.stdout.write("Status: [")
	startTime = time.clock()
	while True:
		buf = HTTPObject.read(block_sz)
		if not buf:
		    break

		file_size_dl += len(buf)
		fileObject.write(buf)
		if (printStatus):
			while (curDot < file_size_dl / dotThresh):
				for e in (25, 50, 75):
					if (curDot == e):
						sys.stdout.write("%s%%" % e)
						curDot = curDot + 3
						continue
				sys.stdout.write("=")
				curDot = curDot + 2
			sys.stdout.flush()
	if (printStatus):
		sys.stdout.write("]\n")
		elapsedTime = time.clock() - startTime
		sys.stdout.write("Finished in %.2f seconds. (%s/second)\n" \
			% (elapsedTime, getInfoString(float(file_size) / elapsedTime)))
	fileObject.close()
	return True

def downloadIndirect(url, referer, saveFile="", \
	overWrite=True, printStatus=True):
	req = urllib.request.Request(url, data=None, \
		headers={"Referer": referer})
	opener = urllib.request.build_opener()
	u = opener.open(req)

	contDisp = u.getheader("Content-Disposition")
	if saveFile is None or saveFile == "":
		if contDisp is None:
			saveFile = url.split('/')[-1]
		else:
			lowIndex = contDisp.find("\"")
			hiIndex = contDisp.find("\"", lowIndex + 1)
			if (lowIndex != -1 and hiIndex != -1):
				saveFile = contDisp[lowIndex + 1: hiIndex]
			else:
				saveFile = url.split('/')[-1]

	if os.path.isfile(saveFile):
		if (overWrite):
			os.remove(saveFile)
			if (printStatus):
				print("Overwriting file: \"%s\"" % saveFile)
		else:
			if (printStatus):
				print("File already exists! Will not download.")
			return False

	return _downloadData(u, saveFile, printStatus)
	

def downloadDirect(url, saveFile="", overWrite=True, printStatus=True):
	if saveFile is None or saveFile == "":
		saveFile = url.split('/')[-1]

	if os.path.isfile(saveFile):
		if (overWrite):
			os.remove(saveFile)
			if (printStatus):
				print("Overwriting file: %s" % saveFile)
		else:
			if (printStatus):
				print("File already exists! Will not download.")
			return False

	u = urllib.request.urlopen(url)

	return _downloadData(u, saveFile, printStatus)

# Unit Tests