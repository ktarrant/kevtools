# Creates a calendar based on UMD Calendar information
# The calendar is a CSV file that can be imported to Google Calendar

import os

class Calendar:

	fields = ("Subject", \
		"Start Date", "Start Time", \
		"End Date", "End Time", \
		"All Day Event", \
		"Description", "Location", \
		"Private")

	filename = ""

	def __init__(self, filename=""):
		""" Creates a Calendar object and attempts to open
			an output file. If the output filename is not
			valid, or if the file is not a valid calendar
			file, the Calendar will output to "temp.csv".
			If the file is a valid calendar file, the
			Calendar will append to the existing calendar. """

		if (filename is None or filename == ""):
			self.createNewCalendar("temp.csv")
		else:
			try:
				f=open(filename, "r")
				if (self.verifyValidCalendar(f) == True):
					f.close()
					self.filename = filename
				else:
					self.createNewCalendar(filename)
			except (FileNotFoundError):
				self.createNewCalendar(filename)

	def verifyValidCalendar(self, fileObject):
		# TODO: add code to validate existing calendars
		return False

	def createNewCalendar(self, filename):
		self.filename = filename
		if os.path.isfile(filename):
			os.remove(filename)
		f = open(filename, "w")
		self.writeCalendarHeaders(f)
		f.close()

	def writeCalendarHeaders(self, fileObject):
		for field in self.fields:
			fileObject.write(field + ", ")
		fileObject.write("\n")

	def edit(self):
		return self.CalendarEditor(open(self.filename, "a"))


	class CalendarEditor:

		fileObject = None

		fields = ("Subject", \
		"Start Date", "Start Time", \
		"End Date", "End Time", \
		"All Day Event", \
		"Description", "Location", \
		"Private")

		def __init__(self, fileObject):
			self.fileObject = fileObject

		def addEvent(self, fields_dict):
			for field in self.fields:
				if field in fields_dict:
					self.fileObject.write(fields_dict[field])
				self.fileObject.write(", ")
			self.fileObject.write("\n")
			return self

		def commit(self):
			self.fileObject.close()


# Testing

