# Pre-processing code to create traingin data for the subset of the Syrian data set

import csv
import ngram
import random


def cal_score(i, j, raw):
	# result = [int(raw[i][-1]==raw[j][-1])]
	result = []
	candidate1 = raw[i]
	candidate2 = raw[j]
	for i in range(min(len(candidate1), len(candidate2))):
		score = ngram.NGram.compare(candidate1[i], candidate2[i], N=5)
		# score = jellyfish.jaro_winkler(unicode(candidate1[i], encoding='utf-8'), unicode(candidate2[i], encoding='utf-8'))
		result.append(score)
	return result


def process():
	cluster = {}
	raw = {}
	identities = {}
	with open('data/syria_train.csv', 'wb') as pair:
		writer = csv.writer(pair, delimiter=',')
		with open('data/ir-for-beka.csv', 'rb') as pairs:
			reader = csv.reader(pairs, delimiter=',')
			header = reader.next()
			i=1
			for row in reader:
				cluster[row[1]+row[2]] = i

				elem = row[3].split(' ')
				if len(elem)>2:

					raw[i] = [elem[0]]+[elem[1]]+[elem[-1]]+[row[4]]+[row[7]]+[row[8]]+[row[9]]
				elif len(elem)==2:
					raw[i] = [elem[0]]+['']+[elem[-1]]+[row[4]]+[row[7]]+[row[8]]+[row[9]]
				else:
					raw[i] = [elem[0]]+['']+['']+[row[4]]+[row[7]]+[row[8]]+[row[9]]

				i+=1

		with open('data/merged-records.csv', 'rb') as merge:
			reader = csv.reader(merge, delimiter='|')
			header = reader.next()
			writer.writerow(header)
			c = 0
			for row in reader:
				members = row[9].split(";")
				count = []
				if len(members)>1:
					for member in members:
						if member in cluster:
							count.append(cluster[member])

					if len(count)>1:
						score = cal_score(count[0], count[1], raw)
						if sum(score)>=6 and c<80000:
							writer.writerow(score+[1]+[count[0], count[1]])
							c+=1

					for a in range(len(count)):
						identities[count[a]] = count
			d = 0
			for i in range(80000):
				a = random.randint(1, len(raw)-1)
				b = random.randint(1, len(raw)-1)
				if (a==b):
					b = random.randint(1, len(raw)-1)
				if (b not in identities) or (a not in identities):
					score = cal_score(a, b, raw)
					if d<80000:
						writer.writerow(score+[0]+[a, b])
						d+=1


def process_data():
	cluster = {}
	with open('data/syria.csv', 'wb') as pair:
		writer = csv.writer(pair, delimiter=',')
		with open('data/ir-for-beka.csv', 'rb') as pairs:
			reader = csv.reader(pairs, delimiter=',')
			header = reader.next()
			writer.writerow(header)

			for row in reader:
				elem = row[3].split(' ')
				if len(elem)>2:

					writer.writerow([elem[0]]+[elem[1]]+[elem[-1]]+[row[4]]+[row[7]]+[row[8]]+[row[9]])
				elif len(elem)==2:
					writer.writerow([elem[0]]+['']+[elem[-1]]+[row[4]]+[row[7]]+[row[8]]+[row[9]])
				else:
					writer.writerow([elem[0]]+['']+['']+[row[4]]+[row[7]]+[row[8]]+[row[9]])

process_data()
process()
