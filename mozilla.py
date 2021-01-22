from __future__ import division, unicode_literals
from html.parser import HTMLParser
import random
import os
import datetime
from os import listdir
from os.path import isfile, join


class FreePlane():
    node = "<map version=\"1.0.1\"><node ID=\"ID_" + str(random.randint(1,2000000000)) +"\" TEXT=\"Imported From Chrome\">"
    insideH3 = False
    insideAnchor = False
    firstHead = True

class MyHTMLParser(HTMLParser):
    def cleanXMLfromSpecialChars(self,line):
        """
        Ampersand	&amp;	&
        Less-than	&lt;	<
        Greater-than	&gt;	>
        Quotes	&quot;	"
        Apostrophe	&apos;	'
        """
        return str(line).replace("&", "&amp;").replace("\"","&quot;").replace("<","&lt;").replace(">","&gt;").replace("'","&apos;")
    def handle_starttag(self, tag, attrs):
        if(tag=="h3"):
            FreePlane.insideH3 = True
            if(FreePlane.firstHead):
                FreePlane.firstHead = False
                FreePlane.node = FreePlane.node + '<node ID=\"ID_' + str(random.randint(1, 2000000000)) + '\"' 
            else:
                FreePlane.node = FreePlane.node + '</node><node ID=\"ID_' +  str(random.randint(1,2000000000)) + '\"'
        if(tag=="a"):
            FreePlane.insideAnchor = True
            FreePlane.node = FreePlane.node + '<node ID=\"ID_' + str(random.randint(1,2000000000)) + '\"'
        for attr in attrs:
            if(attr[0]=='href'):
                FreePlane.node = FreePlane.node + ' LINK=\"' + self.cleanXMLfromSpecialChars(attr[1])  + "\""
    def handle_endtag(self, tag):
        if (tag == "h3"):
            FreePlane.insideH3 = False
        if (tag == "a"):
            FreePlane.insideAnchor = False
            FreePlane.node = FreePlane.node + "/>\n"
    def handle_data(self, data):
        if(FreePlane.insideH3):
            FreePlane.node = FreePlane.node + ' TEXT=\"' + self.cleanXMLfromSpecialChars(data) + "\">"
        elif(FreePlane.insideAnchor):
            FreePlane.node = FreePlane.node + ' TEXT=\"' + self.cleanXMLfromSpecialChars(data) + "\""

# instantiate the parser and fed it some HTML
mindmap = FreePlane()

def getDate():
    today = datetime.date.today()
    now = datetime.datetime.now()
    header_date_time = str(today.day)+  "-" + now.strftime("%B") + "-" + str(today.year)
    return header_date_time
def importFromChrome():
    onlyfiles = [f for f in listdir(str(os.curdir)) if isfile(join(str(os.curdir), f))]
    count_html = 0
    input_file_name = ""
    input_file_not_found_flag = True
    for file in onlyfiles:
        if '.html' in file:
            count_html += 1
            input_file_not_found_flag = False
            input_file_name = file
    if count_html > 1:
        print("More than 1 input files found")
        a = input()
        return a
    if input_file_not_found_flag:
        print("No input File found")
        a = input()
        return a
    input_fh = open(input_file_name, 'r', encoding="UTF-8")
    outputFileName = 'BookmarksFromMozilla(' + getDate() + ').mm'
    output_fh = open(outputFileName, "w", encoding="UTF-8")
    print("Generated file:" + outputFileName)


    parser = MyHTMLParser()

    parser.feed(input_fh.read())
    input_fh.close()
    mindmap.node = mindmap.node + "</node></node></map>"

    output_fh.writelines(mindmap.node)
    output_fh.close()
    return


importFromChrome()
print("Bookmarks Imported.\n")
print("Press any key to continue.\n")
a = input()