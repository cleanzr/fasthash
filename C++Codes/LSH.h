#pragma once
#include "Bucket.h"

class LSH {
private:
	Bucket **_bucket;
	int _K;
	int _L;
	int *rand1;
public:
	LSH(int K, int L);
	int static _rangePow;
	int static _thresh;
	void add(int *hashes, int id);
	int * retrieve(int *hashes);
	~LSH();
}; 
