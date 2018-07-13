#!/usr/bin/env python

#------------------------------------------------------------------------
# percenterror.py
# author: Karbo
# date: Summer
# edited: 12 July 2018
#
#This code calculates the percent error between two columns of values.
#It is meant to be used with the output from an FBM "net-pred btd" command.
#------------------------------------------------------------------------

import numpy
import sys

name = sys.argv[1]

a, b, c = numpy.loadtxt( name, unpack=True)
error = numpy.mean(abs(( b - a ) / a) * 100)
print error
