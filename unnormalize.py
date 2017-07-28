#!/usr/bin/env python

#------------------------------------------------------------------------
#unnormalize.py, a code written by Karbo in the summer of 2017.
#This code unnormalizes a datafile that it is given.
#It assumes that the file is divided into columns with the first line of each
#column containing the header. The first argument is the data to unnormalize.
#The the second and third tell the program where to find the standard devaition
#and mean by reading first the filename and then the integer number of the column 
#the program should use. The pgogram assumes it is using a file generated
#from the normalize.py program.
#------------------------------------------------------------------------

import sys
import linecache
import math

def main():
    name = sys.argv[1] #read data filename from the terminal
    name2 = sys.argv[2] #read info filename from terminal
    num = int(sys.argv[3])#read which mean and std value to use
    datafile = open(str(name), 'r') #open the data file
    infofile = open(str(name2), 'r') #open the info file
    outfile = open('un-normalized_'+str(name), 'w') #open a file to write normalized data

    line = linecache.getline(str(name2), 1)
    mean = line.split()[num]
    line = linecache.getline(str(name2), 2)
    std = line.split()[num]
    
    infofile.close()

    line = datafile.readline() #get a line
    cols = len(line.split()) #find number of columns in file

    for i, l in enumerate(datafile): 
        pass
    rows = i + 1 #find number of rows in file

    print('\nFile profiled: '+str(cols)+' columns '+str(rows)+' lines\n')
    
    value = [[] for i in xrange(cols)] #list of values [column][row]
    col_width = [[] for i in xrange(cols)] #width of each column [column]
    label = [[] for i in xrange(cols)] #name of each column [column]

    row = linecache.getline(str(name), 1) #get first line
    for i in range(cols):
        label[i] = str(row.split()[i]) #read first line for column names

    for j in range(rows):
        row = linecache.getline(str(name), j+2) #get the line j
        for i in range(cols):
            value[i].append(row.split()[i]) #read ith value of j into [i][j]
            value[i][j] = (float(value[i][j]) * float(std)) #multiply by std
            value[i][j] = value[i][j] + float(mean) #add mean
            value[i][j] = str(value[i][j]) #convert value to a str so it has a length
        
    datafile.close()
    print "Values un-normalized\n"
    print "mean: " + mean + "\n"
    print "std: " + std + "\n"

#write column labels
    for i in range(cols):
        col_width[i] = len(max(value[i], key=len))+3 #find the max length of each column
        outfile.write("{0:>{1}}".format(label[i], col_width[i]))
        outfile.write("  ")
    outfile.write("\n")

#write column values
    for j in range(rows): 
        for i in range(cols):
            outfile.write("{0:>{1}}".format(str(value[i][j]), col_width[i]))
            outfile.write("  ")
        outfile.write("\n")
    
    outfile.close()
    print('Un-normalized data written to '+'un-normalized_'+str(name) + '\n')

main()
