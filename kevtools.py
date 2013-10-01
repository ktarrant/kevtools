#!/usr/bin/env python

import sys
from cmdline import CommandLineCaller
import it_ebooks
import download
import calscripts


mycaller = CommandLineCaller(sys.argv[0])
mycaller.createCommandFunction("download-ebook", it_ebooks.downloadEbook)
mycaller.createCommandFunction("download-ebook-all", \
	it_ebooks.downloadAllEbooks)
mycaller.createCommandFunction("download download-direct", \
	download.downloadDirect)
mycaller.createCommandFunction("download-indirect", download.downloadIndirect)
mycaller.createCommandFunction("calendar-academic", \
	calscripts.createAcademicCalendar)


mycaller.callFromArgument(sys.argv[1:])