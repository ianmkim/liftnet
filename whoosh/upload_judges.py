from app import *
import csv

def read_from_file(name="names.csv"):
	judges = []
	with open(name) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			print(row[0].split()[0] + row[0].split()[1])

			judges.append({"firstname":row[0].split()[0] , "lastname": row[0].split()[1], "paradigm":row[1]})

	return judges


def upload_to_database():
	judges = read_from_file()
	count = 0
	total = len(judges)
	for judge in judges:
		judgeObj = Judge(firstname=judge['firstname'],
			lastname=judge['lastname'],
			paradigm=judge['paradigm'])
		db.session.add(judgeObj)
		db.session.commit()
		count+=1
		print("uploaded {0}/{1}".format(count, total))


upload_to_database()