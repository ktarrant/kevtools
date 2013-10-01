import urllib.request
from calendar import Calendar
import locale

months = ["January", "February", "March", "April", "May", "June", "July",
			"August", "September", "October", "November", "December"]

def grabEnclosedString(content, cur, tag):
	size = cur
	cur = content.find("<" + tag, cur)
	if cur == -1: return cur
	cur = content.find(">", cur) + 1
	end = content.find("</" + tag + ">", cur)
	size = end + len("</" + tag + ">") - size
	return (content[cur:end], size)

def parseAndAdd(label, date, year, cal):
	date_sp = date.split(" ")

	multi_month = False
	ranged = False
	st_month = months.index(date_sp.pop(0)) + 1
	st_date = ""
	en_month = ""
	en_date = ""

	dt = date_sp.pop(0)
	while dt == "":
		dt = date_sp.pop(0)

	dt_sp = dt.split("-")
	if len(dt_sp) > 1:
		ranged = True
		st_date = dt_sp[0]

		if months.count(dt_sp[1]) > 0:
			en_month = months.index(dt_sp[1]) + 1
			multi_month = True
		else:
			en_month = st_month
			en_date = int(dt_sp[1])
	else:
		st_date = int(dt_sp[0])

	if (multi_month):
		dt = date_sp.pop(0)
		while dt == "":
			dt = date_sp.pop(0)
		en_date = int(dt)

	st_str = str(st_month) + "/" + str(st_date) + "/" + str(year)

	if ranged:
		en_str = str(en_month) + "/" + str(en_date) + "/" + str(year)
	else:
		en_str = ""

	edit = cal.edit()
	edit.addEvent({"Subject": label, \
		"Start Date": st_str, "End Date": en_str, \
		"All Day Event": "True"}).commit()


def createAcademicCalendar(year, filename=""):
	#cal = Calendar(filename)
	year = int(year)
	yearSuffix = year % 100
	url = "http://www.provost.umd.edu/calendar/%d.html" % yearSuffix

	content = urllib.request.urlopen(url).read()
	encoding = locale.getdefaultlocale()[1]
	content = content.decode(encoding)

	cal = Calendar(filename)

	cur = 0
	state = "SEEK"
	year = 0

	while (cur >= 0 and cur < len(content)):
		if (state == "SEEK"):
			hcur = content.find("<h2>", cur)
			cur = content.find("<tr>", cur)
			if hcur > 0 and hcur < cur:
				hcur = content.find("20", hcur)
				year = int(content[hcur+2:hcur+4])
			state = "READ"
		elif (state == "READ"):
			(block, sz) = grabEnclosedString(content, cur, "tr")
			(label, lsz) = grabEnclosedString(block, 0, "td")
			(date, dsz) = grabEnclosedString(block, lsz, "td")
			cur = cur + sz

			parseAndAdd(label, date, year, cal)

			state = "SEEK"




#createAcademicCalendar("13", "UMD_2013_Calendar.csv")