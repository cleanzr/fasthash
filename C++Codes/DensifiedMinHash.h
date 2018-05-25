#include <iostream>
#pragma once
using namespace std;
class DensifiedMinHash
{private:
	int *_randa, _numhashes, _chunksize, _rep;
	void getFastMinHash(unsigned int *nonZeros, int *hashArray, int randa,int size);
public:
	int static rangePow;
	DensifiedMinHash(int numHashes, int chunksize);
	//	FastMinHash(int seed);
	int * getHash(string filename, int ngrams);
	int * getHash(unsigned int *nonZeros, int size);
	//DensifiedMinHash();
	~DensifiedMinHash();
};

