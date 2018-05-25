#include "DensifiedMinHash.h"
#include <random>
#include <iostream>
#include <climits>
#pragma once
/* Author: Anshumali Shrivastava
*  COPYRIGHT PROTECTION
*  Free for research use.
*  For commercial use, contact:  RICE UNIVERSITY INVENTION & PATENT or the Author.
*/
using namespace std;

DensifiedMinHash::DensifiedMinHash(int numHashes, int chunksize)
{

	_numhashes = numHashes;
	_chunksize = chunksize;
	if (!((_chunksize != 0) && !(_chunksize & (_chunksize - 1)))) {
		cout << "Chunk must be power of 2";
		return;
	}

	_rep = ceil((_numhashes + 0.0) / (chunksize + 0.0));
	_randa = new int[_rep];

	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> dis(1, INT_MAX);

	for (size_t i = 0; i < _rep; i++)
	{
		_randa[i] = dis(gen);
		if (_randa[i] % 2 == 0)
			_randa[i]++;
	}
}



int * DensifiedMinHash::getHash(string record, int ngrams)
{
	//char *rechar = &record[0];

	std::hash<string> stringHasher;
	int length = record.length();
	
	unsigned int *nonzeros = new unsigned int[length - ngrams + 1];
	for (size_t i = 0; i < length - ngrams + 1; i++)
	{
		/*char *substr = new char[ngrams];
		memcpy(substr, &rechar[i], ngrams);
		unsigned int strhash = 0;
		while (*substr)
		{
			strhash = strhash * 101 + *substr++;
		}*/
		
		string str = record.substr(i, ngrams);
		unsigned int strhash = (stringHasher(str));
		nonzeros[i] = strhash;
	}

	return getHash(nonzeros, length - ngrams + 1);

}

int * DensifiedMinHash::getHash(unsigned int *nonZeros, int size)
{
	int *hashes = new int[_rep*_chunksize];
	for (size_t i = 0; i < _rep; i++)
	{
		getFastMinHash(nonZeros, &hashes[i*_chunksize], _randa[i], size);
	}

	return hashes;
}

void DensifiedMinHash::getFastMinHash(unsigned int *nonZeros, int *hashArray, int randa, int sizenonzeros)
{
	unsigned int *hashes = new unsigned int[_chunksize];

	int range = 1 << DensifiedMinHash::rangePow;
	int binsize = range / _chunksize;

	for (size_t i = 0; i < _chunksize; i++)
	{
		hashes[i] = UINT_MAX;
	}

	for (size_t i = 0; i < sizenonzeros; i++)
	{
		
		unsigned int h = nonZeros[i];
		//h ^= h >> 16;
		h *= randa;
		h ^= h >> 13;
		h *= 0x85ebca6b;
		int curhash = ((unsigned int)(((unsigned int)h*nonZeros[i]) << 5) >> (32 - DensifiedMinHash::rangePow));
		int binid = floor(curhash / binsize);
		//cout << binid << endl;
		if (hashes[binid] > curhash)
			hashes[binid] = curhash;
	}


	int *rothashes = new int[2 * _chunksize];

	for (size_t i = 0; i < _chunksize; i++)
	{
		rothashes[i] = hashes[i];
		rothashes[_chunksize + i] = hashes[i];
	}

	for (int i = 2 * _chunksize - 2+1; i >= 0; i--)
	{
		if (rothashes[i] == UINT_MAX)
			rothashes[i] = rothashes[i + 1] + binsize;
	}

	for (size_t i = 0; i < _chunksize; i++)
	{
		hashArray[i] = rothashes[i];
		//cout << hashArray[i] << endl;
	}

}

DensifiedMinHash::~DensifiedMinHash()
{
	delete[] _randa;
}
