#!/usr/bin/env python

#------------------------------------------------------------------------
#normalize.py, a code written by Karbo in the summer of 2017.
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
    outfile = open('smooshed_'+str(name), 'w') #open a file to write normalized data

    line = infile.readline() #get a line
    cols = len(line.split()) #find number of columns in file

    for i, l in enumerate(infile): 
        pass
    rows = i + 1 #find number of rows in file

    print('\nFile profiled: '+str(cols)+' columns '+str(rows)+' lines\n')
    
    value = [[] for i in xrange(cols)] #list of values [column][row]
    valuenew = [[] for i in xrange(cols)] #list of new values [column][row]
    valuesqr = [[] for i in xrange(cols)] #list of squared values [column][row]
    mean = [[] for i in xrange(cols)] #list of mean of each column [column]
    meansqr = [[] for i in xrange(cols)] #list of mean of the squared values [column]
    std = [[] for i in xrange(cols)] #standard deviation of each column [column]
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
        mean[i] = sum(float(a) for a in value[i])/rows #calulate mean for each column
        for j in range(rows):
            valuenew[i].append(float(value[i][j]) - mean[i]) #subtract the mean from the value
            valuesqr[i].append(valuenew[i][j] * valuenew[i][j]) #square the new value
        meansqr[i] = sum(float(a) for a in valuesqr[i])/rows #calculate mean of sqrvalues
        std[i] = math.sqrt(meansqr[i]) #take the sqrt of the mean which is the std
        col_width[i] = len(max(value[i], key=len))+3 #find the max length of each column

    print "Calculations complete\n"



#write column means
    outfile.write ("Mean: ")
    for i in range(cols):
        outfile.write("{0:>{1}}".format(str(mean[i]), col_width[i]))
        outfile.write("  ")
    outfile.write("\n")

#write column stds
    outfile.write ("Std:  ")
    for i in range(cols):
        outfile.write("{0:>{1}}".format(str(std[i]), col_width[i]))
        outfile.write("  ")
    outfile.write("\n\n")

#write column labels
    outfile.write("      ")
    for i in range(cols):
        outfile.write("{0:>{1}}".format(str(label[i]), col_width[i]))
        outfile.write("  ")
    outfile.write("\n")

#write column values
    for j in range(rows): 
        outfile.write("      ")
        for i in range(cols):
            value[i][j] = float(value[i][j]) / std[i]
            outfile.write("{0:>{1}}".format(str(value[i][j]), col_width[i]))
            outfile.write("  ")
        outfile.write("\n")
    
    outfile.close()
    print('Smooshed data written to '+'smooshed_'+str(name) + '\n')

main()
