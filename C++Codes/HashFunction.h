#pragma once
#include <iostream>
using namespace std;
class HashFunction
{
public:
	virtual int * getHash(string filename, int ngrams) = 0;
	virtual int * getHash(unsigned int *nonZeros,int size) = 0;
};

