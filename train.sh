#------------------------------------------------------------------------
#train.sh, a code written by Karbo in the summer of 2017.
#This code trains BNNs with Radford Neal's FBM software.
#The code assumes that fbm is in the user's path.
#The file takes three arguments, the name of the output file, the number
#of points to use, and the number of cycles to use. This code requires the 
#datafile to be configured manually (so that multiple network can be trained
#off the same data quickly) and uses a hybrid montecarly for a linear
#regression problem. It also assumes that the user requires 19 inputs and 
#one target, as is the case in pMSSM. The code also currently emails the results
#to me, so please either delete that part or change the email address if you
#plan to use the code :)
#See FBM's documentation for more info
#------------------------------------------------------------------------
name=$1 #first argument is the name
points=$2 #second argument is the number of points
cycles=$3 #third argument is the number of cycles

net-spec $name 19 10 1 / - 0.05:0.5 0.05:0.5 - x0.05:0.5 - 100 #create network specs
model-spec $name real 0.05:0.5 #specify the model

#specificy the datafile and lines to use
data-spec $name 19 1 / normalized_55201points.dat@5:$(( $points + 4 )) . normalized_55201points.dat@54202:55201 .

#run the network for a short time to get good values for the hyper-parameters
net-gen $name fix 0.5
mc-spec $name repeat 10 sample-noise heatbath hybrid 100:10 0.2
net-mc $name 1

#train the network and send an email wiht the error analysis when complete
mc-spec $name sample-sigmas heatbath hybrid 1000:10 0.4
(net-mc $name $cycles ; net-pred td $name 101:%$(( ($cycles + (200 - 1)) / 200)) | mail -s "Network $name has finished training!" alexanderkarbo@gmail.com) & 
