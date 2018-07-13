#------------------------------------------------------------------------
# file: train.sh
# author: Karbo
# date: summer 2017
# edited: M.P. Kuchera 11 July 2018
#
# breif: This code trains BNNs with Radford Neal's FBM software.
# https://www.cs.toronto.edu/~radford/fbm.software.html
#
# The code assumes that fbm is in the user's path.
# The file takes 4 arguments, the name of the output file, the datafile, the number
# of points to use, and the number of cycles to use. The script uses a hybrid montecarlo for a linear
# regression problem. It also assumes that the user requires 19 inputs and
# one target, as is the case in the pMSSM.
#
# See FBM's documentation for more info
#
# the next three lines have some saved values for priors:
# 19 20 1 / - 0.05:0.5 0.05:0.5 - x0.05:0.5 - 100
# 19 20 20 1 / - 0.05:1:1.5 0.2:1 - x0.3:1 - 0.2:1 -  x0.1:1:4 - - 10
# 19 10 10 10 1 / - 0.05:1:1.5 0.2:1 - x0.3:1 - 0.2:1 -  x0.1:1:4 - 0.2:1 -  x0.1:1:4 - - 10
#----------------------------------------------------------------------

name=$1 #first argument is the network file name
data=$2 # datafile path and name
points=$3 #second argument is the number of points to use in training
cycles=$4 #third argument is the number of cycles to run HMC algorithm


echo "data file is $data"
counter=1
while [ $counter -le 1 ] # changed from 10. Can do more for statistics -- std dev, etc
do
    echo "counter = $counter"
    #let "min = $((85764 + $(($counter * 1000)) ))" #This is the variable for where the testing points start
    #let "max = $(( $min + 999 ))"   #This is the variable for where the testing points end
    let "min = 3001"
    net-spec $name.net 19 20 20 20 1 / - 0.05:1:1.5 0.2:1 - x0.3:1 - 0.2:1 -  x0.3:1 - 0.2:1 -  x0.1:1:4 - - 10 #specify the network architecture
    model-spec $name.net real 0.05:0.5 #specify model -- real = regression
    data-spec $name.net 19 1 / $data@4:$(($points+4)),21 . $data@$min:$max,21 . #specify data
    echo "Done setting up network"
    net-spec $name
    #do some set up and then specify the training
    net-gen $name.net fix 0.5
    mc-spec $name.net repeat 10 sample-noise heatbath hybrid 100:10 0.2
    net-mc $name.net 1
    mc-spec $name.net sample-sigmas heatbath hybrid 1000:10 0.4
    echo "Done setting up MC"
    #below is the training and analysis. the command first trains a network, then generates a prediction from it and writes it to a text file. The test data is then un-normalized and written to another file.
    net-mc $name.net $cycles
    echo "done training"
    (net-pred tdb $name.net $(( $cycles - (($cycles * 4) / 5 ) )):%$(( ($cycles + (200 - 1)) / 200)) >> $name.txt
    python ../unnormalize.py $name.txt $data 20
    #The percent error is then calculated and emailed to me
    python ../percenterror.py un-normalized_$name.txt | mail -s "Percent error for $name after un-normalization" mikuchera@davidson.edu)
    python ../percenterror.py un-normalized_$name.txt >> un_norm_error.txt

    ((counter++))
done
