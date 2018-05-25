 Unique Entity Estimation Package (UEE package)
 =============
 
 #### Introduction
 
 The [Unique Entity Estimation Algorithm](http://arxiv.org/abs/1305.6659) is a way of tackling a sub-task of entity resolution (record linkage or de-duplication), namely unique estimation with associated standard error of these estimates. 
Unique entity estimation shares many fundamental challenges of entity resolution, namely, that the computational cost of all-to-all entity comparisons is intractable for large databases. To circumvent this computational barrier, we propose an efficient (near-linear time) estimation algorithm based on locality sensitive hashing (LSH). Our estimator, under realistic assumptions, is unbiased and has provably low variance compared to existing random sampling based approaches. In addition, we empirically show its superiority over the state-of-the-art estimators on three real applications. We also apply our estimator to a subset of the Syrian conflict (March 2011 -- April 2014), where our results are very similar in nature to those of the Human Rights Data Analysis Group (HRDAG), which have provided us with the data and we use to benchmark our methodology and algorithms. For the full details of our paper, please refer to and cite [Chen, Shrivastava, Steorts (2018), To Appear, AoAS](https://arxiv.org/abs/1710.02690). Efficient C++ and Python code is provided on this repository. In addition, we provided the two public data sets and code to reproduce our LSHE estimates for full transparency and reproducibility. If one has access to the two private data sets from our paper, our code will reproduce these as well. All pre-processing scripts are included for full reproducibility and transparency. 

#### Usage

1. Clone this repository:
	<pre>
    git clone https://github.com/RUSH-LAB/LSHUniqueEntityEstimator.git
  </pre>
  
2. Installation

This package is written in C++ and Python. We require at least g++ version 5 and python 2.7. 

3.  Prerequisites

The following packages are needed in Python for the code to run: 

```
C++, Python 2, ngram, sklearn, numpy, scipy, matlib
```

Remark: In order to install using pip, one will need to run the following commands if errors arise from the terminal due to recent changes with SSH in pip (Linux and MacOS)

```
pip install --pre subprocess32
pip2 install numpy scipy matplotlib
```

4. Compile the minhash package (C++ code):

```
cd C++Codes
g++ -std=c++11 *.cpp -fopenmp (on Windows and Linux)
g++ *.cpp -fopenmp (on MacOS) 
```

Remark: For mac users, the g++ version needs to be 5 or higher.

5. Now, you should be ready to run the package! 

#### Unique Entity Estimation Example

We present detailed steps to replicate the LSHE for the Restaurant data set presented in [Chen, Shrivastava, Steorts (2018), To Appear, AoAS](https://arxiv.org/abs/1710.02690). In addition, we provide a bash script that replicates the LSHE method for all data sets. 

The data sets from the paper that are publicly available can be found in data/ (References from the data sets can be found in our paper). `Restaurant.csv` contains the duplicated entities from the Restaurant data set and 
`Restaurant_pair.csv` contains the corresponding matching pairs of records. `Cd.csv` contains the duplicated entities from the CD data set and `cd_gold.csv` contains the corresponding matching pairs of records. The configuration files to run both of these data sets are `config_restaurant.txt` and `config_cd.txt`

An example of what one row of this record looks like is give below: 

```
"arnie morton's of chicago","435 s. la cienega blv.","los angeles","american",'0'
```

Use the C++ Package folder in this repository. This is a fast minhash package which will take the dataset as input. It will output candidate pairs which fall into blocks (buckets or bins). Using the `Restaurant.csv`, we can get the output file 
`Restaurant_out.csv` in order to perform unique entity estimation. We outline these step below using the Config file from the minhash package. 


1. Update the Config file for minhash and run the program (Remember to change the outputfile name option to Restaurant_pair.csv or the particular name of your data set.) The second and third arguments are K and L respectively.
```
./a.out Config.txt 1 10
```

The output is `Restaurant_pair.csv` where the output is candidate record pairs:

```
Rec1 Rec2
1 2
2 3
...
```

3. Next, we feed in `Restaurant_pair.csv` and `Restaurant.csv` to our UEE algorithm as given below,
where there are many customizable options. 

```
Python pipeline.py --input Restaurant_pair.csv --goldstan data/Restaurant.csv --output any_custom_file_name
```


Other options that one can change include the following:
```
'--trainsize', default='0.1', help='percentage of total pairs to use in training'
'--iter', default='100', help='iterations you want to repeat the process'
'--delimiter', default=',', help='delimeter of input file'
```
*Noted in the delimiter option, the default delimiter for "--goldstan" file is ",", if your file uses different delimiter, which needs to be set here.

The output of this will be the ratio of samples produces from step 2, estimation of the number of unique records in the data set (Restaurant.csv in this example). The output will appear as the following: 


Example output is the following: 

ID RR (reduction ratio) LSHE 
```
1 0.1 742.750000
```

LSHE is the proposed estimator. RR is the reduction ratio of the number of sampled pairs used in the estimation out of total possible pairs.

#### Unique Entity Estimation Script

For better usabiity, an example script `run_script.sh` produces the estimation of our LSHE estimates very similar to our paper as well as our LSHE plots. This script will run all four data sets, assuming the user has access to the two public data sets and two private data sets. To run the script, simply change into the main directory and them run

```
bash run_script.sh
```

Remark:  Here,  "--id" option needs to change when the parameters setting for Config.txt changes to produce the plot in the paper. 


#### Citation

If you use our UEE algorithm package for a paper/project in academic, please use the following BibTeX entry for citation. If you are interested in using our package for propriety/industrial work, please contact the authors on the paper and the Rice/Duke licensing offices and the authors on the packages Beidi Chen (Rice), Anshumali Shrivastava (Rice), and Rebecca C. Steorts (Duke). 

```
@article{chen17unique,
Author = {Beidi Chen and Anshumali Shrivastava and Rebecca C. Steorts},
Title = {Unique Entity Estimation with an Application to the Syrian Conflict},
Year = {2018},
Journal = {Annals of Applied Statistics, To Appear}}
```
