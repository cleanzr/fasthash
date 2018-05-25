# Function that plots the log RE versus the percent sampler size for the LSHE
# Written by BC and RCS
# Input: inputfile (raw data)
# Output: plot of the log RE versus the percent sampler size for the LSHE

import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt

def main():
	parser = argparse.ArgumentParser(description='Process.')
	parser.add_argument('--input', help='input file name')
	parser.add_argument('--gt', help='ground truth for unique entity estimation')
	args = parser.parse_args()
	plot(args.input, int(args.gt))

# plot the log RE versus the percent sample size
def plot(inputfile, gt):
	data = np.genfromtxt(inputfile, delimiter=' ')

	color = ['b', 'g', 'r', 'm', 'y', 'k', 'c', 'b', 'g', 'r']
	dic = set(data[:, 0])

	x = []
	y1 = []
	y2 = []
	y1_bar = []
	y2_bar = []

	for i in range(0, len(dic)):
		cur = list(dic)[i]
		iters1 = data[data[:, 0]==cur,:]

		rr = iters1[:, 1]
		#a = iters1[:, 2]
		b = iters1[:, 2]

		x.append(np.average(rr))
		#y1.append(abs(np.ma.masked_invalid(a).mean()-gt)/gt)
		y2.append(np.average([abs(1.0*elem-gt)/gt for elem in b if elem!='Inf']))
	
	d = list(np.argsort(x))
	x = np.array(x)[d]
	#y1 = np.array(y1)[d]
	y2 = np.array(y2)[d]
	print x
	print y2
	#plt.scatter(x, y1, linestyle=":", label='PRSE')
	plt.semilogy(x, y2, linestyle="-", label='LSHE')

	legend = plt.legend(loc='upper right', shadow=True)
	plt.ylabel('RE')
	plt.xlabel('Samples (%)')
	plt.show()


if __name__ == "__main__":
	main()



