#!/usr/bin/env python

"""ProofOfConcept.py: Used to search for flaws in the ListExpress algorithm"""

import random
import csv
import math
import scipy.stats
import os
import errno
import sys

#GLOBAL CONSTANTS
#Predefined Parameters
FILE = "ProofOfConcept.txt"

class Comparison:
    #Default constructor
    def __init__(self, trueVotesIn, falseVotesIn, indexIn):
        self.greater = None
        self.lesser = None
        self.trueVotes = trueVotesIn
        self.falseVotes = falseVotesIn
        self.weight = calcWeight(self.trueVotes, self.falseVotes)
        self.implemented = False
        self.rejected = False
        self.relationIndex = indexIn
        self.relationTrue = (self.trueVotes >= self.falseVotes)

    #Function to print information about the comparison
    def output(self):
        print(str(self.greater) + " > " + str(self.lesser) + "\t\t" + str(self.weight))

    #Set function for greater
    def setGreater(self, numIn):
        self.greater = numIn
    #Get function for greater
    def getGreater(self):
        return self.greater

    #Set function for lesser
    def setLesser(self, numIn):
        self.lesser = numIn
    #Get function for lesser
    def getLesser(self):
        return self.lesser

    #Set function for greater
    def setWeight(self, weightIn):
        self.weight = weightIn
    #Get function for weight
    def getWeight(self):
        return self.weight

    #Set function for implemented
    def setImplemented(self, boolIn):
        self.implemented = boolIn
    #Get function for implemented
    def getImplemented(self):
        return self.implemented

    #Set function for rejected
    def setRejected(self, boolIn):
        self.rejected = boolIn
    #Get function for rejected
    def getRejected(self):
        return self.rejected

    #Set function for relationTrue
    def setRelationTrue(self, boolIn):
        self.rejected = boolIn
    #Get function for relationTrue
    def getRelationTrue(self):
        return self.rejected

class Test:
    #Default constructor
    def __init__(self):
        self.numElts = 0
        self.comparisons = []
        self.hasse = []
        self.relationDict = {}

    #Creates and populates the relation dictionary based on number of elements (Forward direction).
    def buildDict(self):
        theTot = 0
        for i in range(self.numElts - 1):
            for j in range(i + 1, self.numElts):
                print str(theTot) + " \t" + str(i) + " \t" + str(j)
                self.relationDict[theTot] = (i,j)
                theTot += 1
        print("")

    #Creates the most satisfiable hasse diagram from the given comparison data
    def buildHasse(self):
        pass

    #Set function for numElts
    def setNumElts(self, numIn):
        self.numElts = numIn
    #Get function for numElts
    def getNumElts(self):
        return self.numElts

    #Set function for relationDict
    def setRelationDict(self, dictIn):
        self.relationDict = dictIn
    #Get function for relationDict
    def getRelationDict(self):
        return self.relationDict

    #Set function for comparisons
    def setComparisons(self, comparisonsIn):
        self.comparisons = comparisonsIn
    #Get function for comparisons
    def getComparisons(self):
        return self.comparisons
    #Function to append a Comparison to the end of comparisons
    def addComparison(self, comparisonIn):
        self.comparisons.append(comparisonIn)
    #Function to print information for each Comparison
    def printComparisons(self):
        for comp in self.comparisons:
            comp.output()
        print("")

def main():
    random.seed("0")
    theTest = Test()
    fileIn(theTest)
    theTest.buildDict()

    #Iterates through the dictionary and updates each Comparison with its "definition"
    for i, pair in theTest.getRelationDict().iteritems():
        if theTest.getComparisons()[i].getRelationTrue():
            greaterVal = pair[0]
            lesserVal = pair[1]
        else:
            greaterVal = pair[1]
            lesserVal = pair[0]
        theTest.getComparisons()[i].setGreater(greaterVal)
        theTest.getComparisons()[i].setLesser(lesserVal)

    #Sorts the comparison list, printing some of the information before and after
    theTest.printComparisons()
    theTest.setComparisons(sorted(theTest.getComparisons(), key=lambda comp: comp.getWeight(), reverse=True))
    theTest.printComparisons()

    #theTest.buildHasse()

def fileIn(test):
    data = open(FILE, 'rb')
    reader = csv.reader(data)
    rowNum = 0
    manualMode = False
    maxVotes = 0

    for row in reader:

        #File input functionality will be described in the readme.
        if rowNum == 0:
            if row[0] == 'm':
                manualMode = True
            elif row[0] == 'r':
                manualMode = False
            else:
                print("ERROR: Specify either MANUAL MODE ('m') or RANDOM MODE ('r') in row 0, col 0")
                exit()
        elif rowNum == 1:
            test.setNumElts(int(row[0]))
            if not manualMode:
                maxVotes = int(row[1])

        #NOTE: The code to populate in either mode assumes perfectly formatted data.
        #Populates self.comparisons for manual mode
        else:
            test.addComparison(Comparison(int(row[1]), int(row[0])), (rowNum - 2))
        rowNum += 1

        #Populates self.comparisons for random mode
        if not manualMode:
            for i in range(getNumMatrixRows(test.getNumElts())):
                test.addComparison(Comparison(random.randint(0, maxVotes), random.randint(0, maxVotes), i))

    return

#Returns the number of rows necessary for this program to represent an NxN matrix as a ROWSx2 matrix
def getNumMatrixRows(sideLength):
    return ((sideLength * sideLength - sideLength) / 2)

#This function calculates the weight of a comparison based on the vote information
def calcWeight(tVotes, fVotes):
    total = tVotes + fVotes

    theMax = float(max(tVotes, fVotes))
    weight = 0

    #As long as both the true and false votes are not zero, weight is nonzero
    if total != 0:
       deviation  = (theMax / total) - 0.5

       #math.log is base e (ln)
       weight = deviation * math.log(total)

    return weight

main()