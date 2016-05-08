#!/usr/bin/env python

"""ProofOfConcept.py: Used to search for flaws in the ListExpress algorithm"""

import random
import csv
import math
import os
import errno
import sys

#GLOBAL CONSTANTS
#Predefined Parameters
FILE = "ProofOfConcept.txt"

def main():
    #random.seed("PeeleFrederick")
    pairList = fileIn()
    weightList = getWeights(pairList)
    for elt in weightList:
        print elt[1]

def fileIn():
    data = open(FILE, 'rb')
    reader = csv.reader(data)
    rowNum = 0
    manualMode = False
    numElts = 0
    maxVotes = 0
    pairs = []

    for row in reader:
        #The first line describes the mode to use from here on out
        #It will simply be one character: either an 'r' or an 'm'
        #r is random mode, where the initial matrix is generated
        #m is manual mode, where the initial matrix is specified
        #The rest of this should probably just go in the README so I'll stop here.
        if rowNum == 0:
            if row[0] == 'm':
                manualMode = True
            elif row[0] == 'r':
                manualMode = False
            else:
                print("ERROR: Specify either MANUAL MODE ('m') or RANDOM MODE ('r') in row 0, col 0")
                exit()
        elif rowNum == 1:
            numElts = int(row[0])
            if not manualMode:
                maxVotes = int(row[1])

        #This is the functionality for populating during manual mode.
        #It assumes perfectly correct formatting (including num lines)
        #(So will the random mode stuff.  But I can add exceptions later).
        else:
            pair = [row[0], row[1]]
            pairs.append(pair)
        rowNum += 1

        #Populating for random mode.  Same issues.
        if not manualMode:
            for i in range(((numElts * numElts) - numElts) / 2):
                num1 = random.randint(0, maxVotes)
                num2 = random.randint(0, maxVotes)
                pair = [num1, num2]
                pairs.append(pair)

    return pairs

def getWeights(thePairs):
    weightInfo = []
    for i, pair in enumerate(thePairs):
        weightResult = calcWeight(pair)
        weightInfo.append([i, weightResult[0], weightResult[1]])
    return sorted(weightInfo, key=lambda weightInfo: weightInfo[1], reverse=True)

def calcWeight(pairIn):
    falseVotes = int(pairIn[0])
    trueVotes = int(pairIn[1])
    isTrue = (trueVotes >= falseVotes)
    total = trueVotes + falseVotes
    theMax = float(max(trueVotes, falseVotes))

    #As long as both the true and false votes are not zero
    if total == 0:
        deviation = 0
    else:
       deviation  = (theMax / total) - 0.5

    #math.log is base e (ln)
    weight = deviation * math.log(total)

    return [weight, isTrue]

main()