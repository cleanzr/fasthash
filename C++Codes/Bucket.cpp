#include <iostream>
#include "Bucket.h"
#pragma once

Bucket::Bucket()
{
	isInit = -1;
}

Bucket::~Bucket()
{
	delete[] arr;
}
int Bucket::getSize()
{
	return _size;
}
int Bucket::add(int id)
{
	if (isInit == -1) {
		arr = new int[_size];
		for (int i = 0; i < _size; i++)
			arr[i] = 0;
		isInit = +1;
	}
	if (index == _size) {
		int randind = rand() % _size;
		arr[randind] = id;
	}
	else {
		arr[index] = id;
		index++;
	}
	return 1;
}

int Bucket::retrieve(int index)
{
	if (index >= _size)
		return -1;
	return arr[index];
}

int * Bucket::getAll()
{
	if (isInit == -1)
		return NULL;
	return arr;
}
