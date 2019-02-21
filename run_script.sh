# General script to run the public and private data sets
# Written by BC and RCS

#!/bin/bash

g++-7 -std=c++11 C++Codes/*.cpp -o minhash -fopenmp

 For Restaurant
 for ((i=6;i<=25;i+=6)) ; 
 	do for ((j=1;j<=10; j++));
  		do ./minhash config_restaurant.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.3 --input restaurant_pair.csv --goldstan data/restaurant.csv --output log-restaurant ; 
 	done
 done

 python plot.py --input log-restaurant --gt 753

#For CD
# for ((i=6;i<=20;i+=4)) ; 
# 	do for ((j=1;j<=3; j++));
#  		do ./minhash config_cd.txt 1 $i; python pipeline.py --flag 0 --id $i --trainsize 0.5 --input cd_pair.csv --goldstan data/cd.csv --delimiter ';' --output log-cd ; 
# 	done
# done

# python plot.py --input log-cd --gt 9508

#For Voter
# for ((i=25;i<=40;i+=5)) ; 
# 	do for ((j=1;j<=10; j++));
#  		do ./minhash config_voter.txt 4 $i; python pipeline.py --flag 0 --id $i --trainsize 0.1 --input voter_pair.csv --goldstan data/voter.csv --delimiter ',' --c 0.0001 --output log-voter ; 
# 	done
# done

# python plot.py --input log-voter --gt 255447

#For Syria
# python preprocess.py

#for ((i=1;i<=10;i++)) ; 
#	do ./minhash config_syria.txt 15 10; python pipeline_for_syria.py --input syria_pair.csv --output log-syria --rawdata data/syria.csv --goldstandpair data/syria_train.csv; 
#done

#python count.py --input log-syria
