from app import *
from bs4 import BeautifulSoup
import requests
import sys
from urllib.parse import urlparse
import csv
import threading
import time

url = "https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={0}".format(10000)
code = requests.get(url)
soup = BeautifulSoup(code.text, "html5lib")
listItem = []
text = soup.find_all("div", class_="paradigm")[0].text


def scrape_tabroom(idNum):
	url = "https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={0}".format(idNum)
	code = requests.get(url)
	soup = BeautifulSoup(code.text, "html5lib")
	paradigm = soup.find_all("div", class_="paradigm")
	if(paradigm): 
		if(soup.find_all("div", class_="paradigm")[0].text != text):
			name =  (soup.find_all("div", class_="main")[0].find_all('h2')[0].text.replace('Paradigm', ''))
			paradigm = paradigm[0].text
			write_to_file(name, paradigm)
			return name
		else:
			return ("No Paradigm") 

	else:
		return ('no pardigm')

def write_to_file(name, paradigm):
	with open(r'names.csv', 'a') as f:
	    writer = csv.writer(f)
	    writer.writerow([name, paradigm])


def thread(threadName, threadrange, rangeend):
	for i in threadrange:
		if i+24700 == rangeend:
			break
		print("{0}\t{1} - {2} ".format(threadName,scrape_tabroom(i+24700), i+24700))



numThreadsInt = int(sys.argv[1])
numThreadsFloat = float(sys.argv[1])
numSegmentation = 1000000/numThreadsInt
for i in range(numThreadsInt):
	t1 = threading.Thread(target=thread, 
		args=("THREAD{0}".format(i), range(int(numSegmentation)*i, int(numSegmentation)*i+int(numSegmentation)),int(numSegmentation)*i+int(numSegmentation)) )
	t1.start()


