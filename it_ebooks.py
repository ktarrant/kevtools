import os
from cmdline import CommandLineCaller
from download import downloadIndirect
import urllib.request
import locale

def downloadAllEbooks(directory="", startIndex=1):
    counter = int(startIndex)
    rval = True
    while (rval is True):
        print("%d: " % counter, end = "")
        rval = downloadEbook(counter, directory)
        counter += 1
    return "Downloaded %d books." % (counter - 1)
def downloadEbook(pageNum, directory=""):
    if directory is None:
        directory = ""
    elif directory is not "":
        if not directory.endswith("/") and not directory.endswith("\\"):
            directory = directory + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

    url = "http://it-ebooks.info/book/%s/" % pageNum
    u = urllib.request.urlopen(url)
    encoding = locale.getdefaultlocale()[1]
    content = u.read().decode(encoding)

    ind = content.find("<title>")
    lowerInd = ind + len("<title>")
    higherInd = content.find(" - Free Download", ind)
    title = content[lowerInd:higherInd] + ".pdf"

    if title == "IT eBooks.pdf":    # Means we 404'd
        return "Page Not Found"

    ind = content.find("<tr><td>Download:</td><td>")
    ind = content.find("href", ind)
    lowerInd = ind + len("href='")
    ind = content.find("\"", lowerInd)
    higherInd = content.find("'", lowerInd)
    if higherInd == -1:
        if ind == -1:
            return "Parsing error."
        else:
            higherInd = ind
    else:
        if ind != -1 and ind < higherInd:
            higherInd = ind
    content = content[lowerInd:higherInd]
    if content.startswith("/"):
        content = "http://it-ebooks.info" + content
    print("Downloading \"%s\"" % content)
    return downloadIndirect(content, url, directory + title)

# Unit Tests
