*******************************************************************************************************************************
Optimized Record Linkage: Runs on 250,000 Syrian Death records in 40 sec with reporting only 4 million pairs (out of 10 billions) with a recall of 93%. Right now it treats every record as a plain text. This can be improved (stay tuned)

/* Author: Anshumali Shrivastava
*  COPYRIGHT PROTECTION
*  Free for research use.
*  For commercial use, contact:  RICE UNIVERSITY INVENTION & PATENT or the Author.
*/

Please direct all questions to Anshumali Shrivastava firstname(no caps) @ rice.edu

If you find this code useful in any research please cite


Densifying One Permutation Hashing via Rotation for Fast Near Neighbor Search. 
Anshumali Shrivastava and Ping Li.
International Conference on Machine Learning (ICML) 2014.

Improved Densification of One Permutation Hashing. 
Anshumali Shrivastava and Ping Li.
Conference on Uncertainty in Artificial Intelligence (UAI) 2014.

Blocking Methods Applied to Casualty Records from the Syrian Conflict
Peter Sadosky, Anshumali Shrivastava, Megan Price, Rebecca C. Steorts
arXiv:1510.07714   Report 2015

********************************************************************************************************************************


All the parameters are passed using config.txt files.
Read config.txt to understand the parameters and their format. It should be self-explanatory.


To run the package (command line windows)

RUSHLinkage.exe pathtoConfigfile

Example (if both are at same location)

RUSHLinkage.exe Config.txt

If you have the gold standard evaluation file with  ex format 
LineNumber,Match,index1,index2
1,1,189452,265314
2,0,189452,265771
Then run the Evaluate executable as (command line windows)

EvaluateRecordLinkage.exe outputfile evaluationfile

This will output the recall and also a hard pairs file which will show the missed pairs by the package.

If you are not using windows compile the codes (make sure to use -fopenmp and -std=c++11 as the code uses open mp) example
g++ -std=c++11 *.cpp output -fopenmp





