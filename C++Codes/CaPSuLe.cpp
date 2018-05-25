#include <iostream>
#include "LSH.h"
#include "SignedRandomProjection.h"
#include <string>
#include <ctime>
#pragma once

using namespace std;

int CaPSuLeMain(int argc, char* argv[])
{
	//parameters (very critical to set properly)
	int K = 5;
	int L = 20;
	
	//Data
	int dim = 5;
	int noOfData = 4;
	double data[4][5] =
	{
		{ 1,8,12,20,25 },
		{ 5,9,13,24,26 },
		{ 5,9,13,24,26 },
		{ 19,3,4,-13,2 }
	};

	//Create HashTables
	LSH *_Algo = new LSH(K, L);
	SignedRandomProjection *proj = new SignedRandomProjection(dim,K*L);
	for (size_t i = 0; i < noOfData; i++)
	{
		int * hashes = proj->getHash(data[i], dim);
		_Algo->add(hashes, i);
	}


	//Query
	double query1[5] = { 5,9,13,24,26 };
	int *query1hashes = proj->getHash(query1, 5);
	int *retrieved1 = _Algo->retrieve(query1hashes);
	cout << "No of Potential Matches for Query 1: " << retrieved1[0] << endl;
	cout << "Neighbors:" << endl;
	for (size_t i = 2; i < retrieved1[0]+2; i++)
	{
		cout << retrieved1[i] << endl;
	}

	double query2[5] = { 18.3,3.3,4,-12,2 };
	int *query2hashes = proj->getHash(query2, 5);
	int *retrieved2 = _Algo->retrieve(query2hashes);
	cout << "No of Potential Matches for Query 1: " << retrieved2[0] << endl;
	cout << "Neighbors:" << endl;
	for (size_t i = 2; i < retrieved2[0] + 2; i++)
	{
		cout << retrieved2[i] << endl;
	}
	return 0;
}