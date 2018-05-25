import argparse
import csv
from sklearn import linear_model, ensemble, svm
import random
import os.path
import ngram
import unionfind
from math import floor
import datetime
from sklearn.svm import SVC

from random import shuffle

def main():
	parser = argparse.ArgumentParser(description='Process.')
	parser.add_argument('--input', help='file which has all candidate pairs')
	parser.add_argument('--output', help='output file')
	parser.add_argument('--rawdata', help='file which has raw data')
	parser.add_argument('--goldstandpair', help='file that contains all positive and negative pairs')
	parser.add_argument('--delimiter', default=',', help='delimeter of input file')
	parser.add_argument('--trainsize', default='0.1', help='percentage of total pairs to use in training')
	parser.add_argument('--c',default='1', help='SVM hyper paramter')
	args = parser.parse_args()

	#similarity stage
	candidates, matrix, Allpair, Total, raw, goldPairs, negPairs, saved = calculate_sim(args.input, args.rawdata, args.goldstandpair)
	#print "similarity matrix calculated"

	with open(args.output, 'a') as write:
		writer = csv.writer(write, delimiter=' ')
		estimate_hashing = random_forest(matrix, candidates, Allpair, Total, raw, goldPairs,negPairs, saved)
		writer.writerow([estimate_hashing])
		print estimate_hashing


def calculate_sim(inputf, standard, realpair):
	raw = {}
	#read raw data
	Allpair = {}
	with open(standard, 'rb') as pairs:
		reader = csv.reader(pairs, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		reader.next()
		i=1
		for row in reader:
			if row[-1] in Allpair:
				Allpair[row[-1]].append(i)
			else:
				Allpair[row[-1]] = [i]

			raw[i] = row
			i+=1
	Total = len(raw)

	#create labeled pairs
	goldPairs = []
	negPairs = []
	with open(realpair, 'rb') as realpair:
		reader = csv.reader(realpair, delimiter=',')
		reader.next()
		for row in reader:
			if int(row[-3])==1:
				goldPairs.append((int(row[-2]), int(row[-1])))
			else:
				negPairs.append((int(row[-2]), int(row[-1])))
	#read candidate pairs
	shuffle(goldPairs)
	shuffle(negPairs)
	matrix = {}
	candidates = []
	saved = []
	with open(inputf, 'rb') as candidate:
		reader = csv.reader(candidate, delimiter=' ')
		reader.next()
		t = 0
		a = datetime.datetime.now()
		for row in reader:
			t+=1
			candidates.append((int(row[0]),int(row[1])))
			candidate1 = raw[int(row[0])]
			candidate2 = raw[int(row[1])]

			datapoint = cal_score(int(row[0]), int(row[1]), raw)
			saved.append(datapoint)
	return  candidates, matrix, Allpair, Total, raw, goldPairs, negPairs, saved


def random_forest(matrix, candidates, Allpair, Total, raw, goldPairs, negPairs, saved):

	#split the training and testing data
	posnum = 7000
	negnum = 16000
	split = 0.7
	poslist = []
	poslabels = []
	pospair = []

	neglist = []
	neglabels = []
	negpair = []

	trainlist = []
	trainlabels = []
	testlist = []
	testlabels = []

	train_pair = []
	test_pair = []

	randomresultlist = []
	randomresultlabels = []
	random_pair = []

	hashinglist = []
	hashinglabels = []
	hashing_pair = []


	randomlist = {}
	random.shuffle(goldPairs)
	random.shuffle(negPairs)
	#print len(goldPairs)

	new_pos = 0
	for i in range(posnum):
		datapoint = cal_score(goldPairs[i][0], goldPairs[i][1], raw)
		if sum(datapoint)>=6:
			poslist.append(datapoint[:])
			poslabels.append(1)
			new_pos+=1
			pospair.append(goldPairs[i])
	posnum = new_pos

	new_neg = 0
	for i in range(negnum):
		datapoint = cal_score(negPairs[i][0], negPairs[i][1], raw)
		if sum(datapoint)<4:
			neglist.append(datapoint[:])
			neglabels.append(0)
			new_neg+=1
			negpair.append(negPairs[i])
	negnum = new_neg
	print posnum, negnum
	trainlist = poslist[:int(floor(posnum*split))]+neglist[:int(floor(negnum*split))]
	trainlabels = poslabels[:int(floor(posnum*split))]+neglabels[:int(floor(negnum*split))]
	train_pair = pospair[:int(floor(posnum*split))]+negpair[:int(floor(negnum*split))]

	testlist = poslist[int(floor(posnum*split)):]+neglist[int(floor(negnum*split)):]
	testlabels = poslabels[int(floor(posnum*split)):]+neglabels[int(floor(negnum*split)):]
	test_pair = pospair[int(floor(posnum*split)):]+negpair[int(floor(negnum*split)):]

	q = 0
	for i in range(len(candidates)):
		#datapoint = cal_score(candidates[i][0], candidates[i][1], raw)
		datapoint = saved[i]
		hashinglist.append(datapoint[:])
		# hashinglabels.append(datapoint[0])
		hashing_pair.append(candidates[i])
		# print datapoint, candidates[i]

	#train lr
	svmt = linear_model.LogisticRegression(penalty = 'l2', solver='sag',C=0.00035)
	svmt.fit(trainlist, trainlabels)

	#test on testing data
	testresultlist = svmt.predict(trainlist+testlist)

	#test on hashing selection
	hashingselection = svmt.predict(hashinglist)
	Predict_pairs_hashing = sum(hashingselection)

	hashing_recall=0
	hashing_recall = calculate_pr(goldPairs, hashingselection, testresultlist,trainlabels+testlabels, train_pair+test_pair, hashing_pair, raw)
	print hashing_recall
	estimate_hashing = probability(hashingselection, hashing_recall, hashing_pair, raw, train_pair+test_pair, trainlabels+testlabels)

	return estimate_hashing


def cal_score(i, j, raw):
	result = []
	candidate1 = raw[i]
	candidate2 = raw[j]
	for i in range(min(len(candidate1), len(candidate2))):
		score = ngram.NGram.compare(candidate1[i], candidate2[i], N=5)
		result.append(score)
	return result


def probability(result, p, c_pair, raw, pairs, labels):
	cluster = {}
	neighbors = {}
	checklist = []
	j = 0

	for i in range(len(c_pair)):
		if result[i]==1:
			checklist.append(c_pair[i])
		j+=1

	#checklist = sorted(checklist)
	neighbors, u = union_find(checklist, len(raw))
	
	n2 = 0
	n3 = 0
	n4 = 0
	nn = 0
	track = 0
	#print "long"
	for neighbor in neighbors:
		
		if neighbors[neighbor]==1:
			track+=1
		elif neighbors[neighbor]==2:
			n2+=1
		elif neighbors[neighbor]==3:
			n3+=1
		else:
			nn+=1
			
#	n4o = 1.0*n4/(1-((1-p)**3)*(p**3)*4-((1-p)**4)*(p**2)*15- ((1-p)**5)*(p)*6)
	n1 = track-1
	n3o = 1.0*n3/(1 - 3*(1-p)**2*p - (1-p)**3)
	n2o = 1.0*(n2 - n3o*(3*(1-p)**2*p))/p
	n1o = n1 - 2*n2o*(1-p) - 3*n3o*(1-p)**3 - 3*n3o*p*(1-p)**2
	return n1o+n3o+n2o+nn



def calculate_pr(goldPairs, resultlist, testresultlist, labels, test_pair, c_pair, raw):
	TP = 0
	FP = 0
	P = 0
	P = sum(labels)

	c_pair_dic = {}
	indx = 0
	for elem in c_pair:
		c_pair_dic[elem] = indx
		indx+=1

	a=0
	for i in range(len(labels)):
		if labels[i]==1:
			if test_pair[i] in c_pair_dic:
				if resultlist[c_pair_dic[test_pair[i]]]==1:
					a+=1
	# print "hashing recall", a*1.0/P, P, a, sum(resultlist), len(c_pair_dic)

	if a==0:
		return 'inf'
	else:
		return (a*1.0/P)


def union_find(lis, n):
	u = unionfind.unionfind(n+1)
	for pair in lis:
		u.unite(pair[0], pair[1])
	#print "finish"
	return u.sizes(), u

if __name__ == "__main__":
	main()
