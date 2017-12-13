#!/usr/bin/env python

#------------------------------------------------------------------------
#get_distribution.py, a code written by Karbo in the summer of 2017.
#This code normalizes a datafile that it is given.
#It assumes that the file is divided into columns with the first line of each
#column containing the header.
#------------------------------------------------------------------------

import sys
import linecache
import math

def main():
    name = sys.argv[1] #read filename from the terminal
    infile = open(str(name), 'r') #open the data file
    outfile = open('distributed_'+str(name), 'w') #open a file to write data distribution

    line = infile.readline() #get a line
    cols = len(line.split()) #find number of columns in file

    for i, l in enumerate(infile): 
        pass
    rows = i + 1 #find number of rows in file

    print('\nFile profiled: '+str(cols)+' columns '+str(rows)+' lines\n')
    
    value = [[] for i in xrange(cols)] #list of values [column][row]
    col_width = [[] for i in xrange(cols)] #width of each column [column]
    label = [[] for i in xrange(cols)] #name of each column [column]

    row = linecache.getline(str(name), 1) #get first line
    for i in range(cols):
        label[i] = row.split()[i] #read first line for column names

    for j in range(rows):
        row = linecache.getline(str(name), j+2) #get the line j
        for i in range(cols):
            value[i].append(row.split()[i]) #read ith value of j into [i][j]
        
    infile.close()
    print "Values read\n"

    for i in range(cols):
        col_width[i] = len(max(value[i], key=len))+3 #find the max length of each column
	for j in range(rows):
	    value[i][j] = float(value[i][j])

    value = list(map(list, zip(*value)))

    value.sort(key=lambda value:value[19])

    value = list(map(list, zip(*value)))

    print "Calculations complete\n"

#write column labels
    for i in range(cols):
        outfile.write("{0:>{1}}".format(str(label[i]), col_width[i]))
        outfile.write("  ")
    outfile.write("\n")

#write column values
    for j in range(rows): 
        for i in range(cols):
            outfile.write("{0:>{1}}".format(str(value[i][j]), col_width[i]))
            outfile.write("  ")
        outfile.write("\n")
    
    outfile.close()
    print('Data distribution written to '+'distributed_'+str(name) + '\n')

main()
