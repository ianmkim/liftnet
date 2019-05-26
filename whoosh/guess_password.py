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


def stopWatch(value):
    '''From seconds to Days;Hours:Minutes;Seconds'''

    valueD = (((value/365)/24)/60)
    Days = int (valueD)

    valueH = (valueD-Days)*365
    Hours = int(valueH)

    valueM = (valueH - Hours)*24
    Minutes = int(valueM)

    valueS = (valueM - Minutes)*60
    Seconds = int(valueS)


    print (Days,";",Hours,":",Minutes,";",Seconds)




def thread(threadName, threadrange, rangeend):
	for i in threadrange:
		if i == rangeend or i == 98071079:
			print("PASSWORD HASH CRACKED: {0}".format(i))
			exit()
			break

		print("{0} \t {1}".format(threadName, i))




numThreadsInt = int(sys.argv[1])
numThreadsFloat = float(sys.argv[1])
numSegmentation = 100000000/numThreadsInt
threadList =[]


for i in range(numThreadsInt):
	t1 = threading.Thread(target=thread, 
		args=("THREAD{0}".format(i), range(int(numSegmentation)*i, int(numSegmentation)*i+int(numSegmentation)),int(numSegmentation)*i+int(numSegmentation)) )
	threadList.append(t1)
	t1.start()


