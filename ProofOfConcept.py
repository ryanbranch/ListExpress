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

#NOTE: I realize now that I used "-1" as a sort of placeholder value throughout the code as if it would cause things to
#error out like in C++ if I tempted to access a negative index.  Obviously I'm now realizing what a terrible mistake
#this was.  Could easily be the casue of any finnicky bugs.
#NOTENOTE: Upon further inspection it seems like I never actually access indices at ANY variables which I initialized at
#a value of -1.  So I should be safe.  But I'm leaving this just in case until I'm 100% certain.

class Test:
    #MEMBER VARIABLES:
    #Placeholder

    #Default constructor
    def __init__(self):
        self.numElts = 0
        self.pairs = []

    #Creates and populates the relation dictionary based on number of elements.
    def buildDict(self):
        self.relationDict = {}
        theTot = 0
        for i in range(self.numElts - 1):
            for j in range(i + 1, self.numElts):
                print str(theTot) + " \t" + str(i) + " \t" + str(j)
                self.relationDict[theTot] = (i,j)
                theTot += 1

    def buildSet(self, theWeights):
        #Defines an instance of the Sudoku object for the class to use
        self.sudoku = Sudoku(self.numElts)

        for i, weight in enumerate(theWeights):
            #defines voteInfo, a tuple describing inequality between two items
            #The first element is the greater item, the second element is the lesser one
            voteInfo = self.relationDict[weight[0]]
            if weight[1]:
                print(str(i) + ". Choice " + str(voteInfo[0]) + " \t> \tChoice " + str(voteInfo[1]))
                self.sudoku.oneStep(voteInfo[0], voteInfo[1])
            else:
                print(str(i) + ". Choice " + str(voteInfo[1]) + " \t> \tChoice " + str(voteInfo[0]))
                self.sudoku.oneStep(voteInfo[1], voteInfo[0])
            print(str(self.sudoku.boxes) + "\n\n")

    #Set function for numElts
    def setNumElts(self, numIn):
        self.numElts = numIn
    #Get function for numElts
    def getNumElts(self):
        return self.numElts

    #Set function for pairs
    def setPairs(self, pairsIn):
        self.pairs = pairsIn
    #Get function for pairs
    def getPairs(self):
        return self.pairs
    #Function to append a pair to the end of pairs
    def addPair(self, pairIn):
        self.pairs.append(pairIn)

class Sudoku:
    #Default constructor
    def __init__(self, itemCount):
        self.boxes = []
        self.numBoxes = itemCount

        #Initializes itemsLeft as the number of items in the system
        #As positions are confirmed, the items are removed from this list
        self.itemsLeft = []
        for i in range(self.numBoxes):
            self.itemsLeft.append(i)

        for i in range(self.numBoxes):
            self.boxes.append([])
        self.itemsSeen = []
        self.allSeen = False

    #Gets one step closer to figuring out the final order each time it's run with a given input
    #Note: self.boxes is a list in descending order.  So self.boxes[0] is the highest ranked spot
    #As a general rule, if the program hasn't seen an item yet, it will add it to one or more boxes during this function
    #If it has seen the item, it will remove it from zero or more boxes during this function.
    def oneStep(self, greater, lesser):
        print("Pre-operation boxes: " + str(self.boxes))
        """
        gSeen = (greater in self.itemsSeen)
        lSeen = (lesser in self.itemsSeen)

        """
        #This alternative setup used to cause errors.  Now it doesn't so I can probably get rid of the """comments above
        if not self.allSeen:
            gSeen = (greater in self.itemsSeen)
            lSeen = (lesser in self.itemsSeen)
        else:
            gSeen = True
            lSeen = True


        somethingNew = False


        setBounds = False
        #Checks for an invalid attempt
        if self.allSeen:
            highestG = self.getHighestGreater(greater)
            lowestL = self.getLowestLesser(lesser)
            setBounds = True
            #The truth of this boolean defines an invalid attempt, so we return early
            if highestG >= lowestL:
                #NOTE: I have no idea whether this inequality above should contain equals or no.  I think, but uncertain
                print("Invalid attempt detected. Returning early.")
                return


        #If the greater value has been processed before
        if gSeen:

            #Calculates the value of the highest ranked box which contains "greater"
            if not setBounds:
                highestG = self.getHighestGreater(greater)

            #We know that greater is higher rank than lesser, so it can't exist in the lowest unfilled spot
            #This also only applies when lesser is in self.itemsLeft
            if lesser in self.itemsLeft:
                i = self.numBoxes - 1
                while ((len(self.boxes[i]) == 1) and (self.boxes[i][0] not in self.itemsLeft)):
                    i -= 1
                #Note: i could potentially go out of bounds for a completed list
                if greater in self.boxes[i]:
                    self.boxes[i].remove(greater)

            if lSeen:
                #Removes the lesser item from any boxes at or higher than highestG
                for i in range(highestG + 1):
                    if lesser in self.boxes[i]:
                        self.boxes[i].remove(lesser)
            else:
                for i in range(highestG + 1, self.numBoxes):
                    self.boxes[i].append(lesser)
                self.itemsSeen.append(lesser)
                #NOTE: This should be done whenever something is appended to itemsSeen
                somethingNew = True

        #If the lesser value has been processed before
        if lSeen:

            #Calculates the value of the lowest ranked box which contains "lesser"
            if not setBounds:
                lowestL = self.getLowestLesser(lesser)

            #We know that lesser is lower rank than greater, so it can't exist in the highest unfilled spot
            #This also only applies when greater is in self.itemsLeft
            if greater in self.itemsLeft:
                i = 0
                while ((len(self.boxes[i]) == 1) and (self.boxes[i][0] not in self.itemsLeft)):
                    i += 1
                #Note: i could potentially go out of bounds for a completed list
                if lesser in self.boxes[i]:
                    self.boxes[i].remove(lesser)

            if gSeen:
                #Removes the greater item from any boxes at or below lowestL
                for i in range(lowestL, self.numBoxes):
                    if greater in self.boxes[i]:
                        self.boxes[i].remove(greater)
            else:
                for i in range(lowestL - 1, -1):
                    self.boxes[i].append(greater)
                self.itemsSeen.append(greater)
                #NOTE: This should be done whenever something is appended to itemsSeen
                somethingNew = True

        #If neither of the values have been processed before
        if ((not gSeen) and (not lSeen)):
            for i in range(self.numBoxes - 1):
                (self.boxes[i]).append(greater)
                (self.boxes[i+1]).append(lesser)
            (self.itemsSeen).append(greater)
            (self.itemsSeen).append(lesser)
            #NOTE: This should be done whenever something is appended to itemsSeen
            somethingNew = True

        #If we just saw something new, check if we've seen everything
        if ((self.allSeen == False) and (somethingNew)):
            self.allSeen = ((len(self.itemsSeen)) == (self.numBoxes))

        #If all numbers have been seen and something changed, we attempt to narrow down the search
        #NOTE: I would have thought I could have added " and (somethingNew)" to the conditional
        #in order to prevent extraneous cleanup checks but this seems to cause failure.
        #NOTENOTE: Figuring out a way to skip unneeded cleans is a high priority efficiency improvement.
        #For personal reference, such an event occurs at [6. (2 > 3)] of "Peele Frederick"
        if self.allSeen:
            print("Attempting to clean up the boxes")
            self.cleanup()

    def cleanup(self):
        print("Pre-cleanup boxes: " + str(self.boxes))
        leftInit = len(self.itemsLeft)

        #NOTE: I don't think these 2 "-1"s should be a problem
        uniqueItem = -1
        uniqueIndex = -1
        #Locates and saves the position of any item that exists alone in a box
        for i, box in enumerate(self.boxes):
            if ((len(box) == 1) and (box[0] in self.itemsLeft)):
                uniqueItem = box[0]
                uniqueIndex = i

        #Removes any instance of the aforementioned item (if found) except in it's solo box
        if ((uniqueIndex != -1) and (uniqueItem != -1)):
            for i, box in enumerate(self.boxes):
                if ((uniqueItem in box) and (i != uniqueIndex)):
                    box.remove(uniqueItem)
                    #print("Deleted " + str(uniqueItem) + " from box " + str(i))
            self.itemsLeft.remove(uniqueItem)
            print("REMOVED: " + str(uniqueItem) + " from self.itemsLeft")

        #Appearances is a dictionary with numBoxes integer keys
        #Each key corresponds to a 2-length list which designates:
        #(last box seen in, number of times located)
        #So if the second value is 1, then the first value is that item's only box
        appearances = {}

        #Initializes the empty dictionary to count instances of each item
        for i in range(self.numBoxes):
            appearances[i] = [-1,0]

        #Replaces the appropriate values within the lists in appearances to keep track of information
        for i, box in enumerate(self.boxes):
            for j in self.itemsLeft:
                if j in box:
                    appearances[j][0] = i
                    appearances[j][1] += 1

        #Locks in the position of any item that only exists once throughout all of boxes
        for i in range(self.numBoxes):
            if appearances[i][1] == 1:
                self.boxes[appearances[i][0]] = [i]
                self.itemsLeft.remove(i)
                print ("Removed " + str(i) + " from self.itemsLeft")

        #If any progress was made throughout this function, we rerun the function until no progress is made
        #This may seem counterintuitive since much of the code above is written in a more complicated fashion
        #in order to offer slight efficiency savings.  However, in the long run, this allows us to have the most
        #complete data possible when examining the hierarchy of weighted comparisons, allowing the most educated
        #decision to be made at every point
        if len(self.itemsLeft) != leftInit:
            print("RERUN!")
            self.cleanup()
        return

    #Determines the highest ranked box in which the greater item exists
    def getHighestGreater(self, val):
        i = 0
        highG = -1
        while highG == -1:
            if val in self.boxes[i]:
                highG = i
            else:
                i += 1
        #Invariant: highG should not be -1 here EVER. If it is, major problem.
        if highG == -1:
            print("ERROR: highG retained value of -1")
            exit()
        return highG

    #Determines the lowest ranked box in which the lesser item exists
    def getLowestLesser(self, val):
        i = self.numBoxes - 1
        lowL = -1
        while lowL == -1:
            #print("Looking for " + str(val) + " in")
            #print(self.boxes[i])
            #print("i = " + str(i) + "\n")
            if val in self.boxes[i]:
                lowL = i
            else:
                i -= 1
        #Invariant: lowL should not be -1 here EVER. If it is, major problem.
        if lowL == -1:
            print("ERROR: lowL retained value of -1")
            exit()
        return lowL

def main():
    random.seed("Peele Frederick")
    theTest = Test()
    fileIn(theTest)

    #NOTE: WeightList etc. are bad names for these because it's not just a list of weights but a 2d list where the inner list contains weight, among other things.
    #In the future, I can possibly shave down weightlist to not include these weightings used for ordering.  Not quite sure yet.
    weightList = getWeights(theTest.getPairs())

    #Prints some diagnostic output useful for viewing test results.  Will remove eventually
    for elt in weightList:
        print str(elt[0]) + ". " + str(elt[1]) + "  \t" + str(theTest.getPairs()[elt[0]]) + "  \t" + str(elt[2])

    theTest.buildDict()

    theTest.buildSet(weightList)


def fileIn(test):
    data = open(FILE, 'rb')
    reader = csv.reader(data)
    rowNum = 0
    manualMode = False
    maxVotes = 0

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
            test.setNumElts(int(row[0]))
            if not manualMode:
                maxVotes = int(row[1])

        #This is the functionality for populating during manual mode.
        #It assumes perfectly correct formatting (including num lines)
        #(So will the random mode stuff.  But I can add exceptions later).
        else:
            pair = [int(row[1]), int(row[0])]
            test.addPair(pair)
        rowNum += 1

        #Populating for random mode.  Same issues.
        if not manualMode:
            for i in range(getNumMatrixRows(test.getNumElts())):
                num1 = random.randint(0, maxVotes)
                num2 = random.randint(0, maxVotes)
                pair = [num1, num2]
                test.addPair(pair)

    return

#Returns the number of rows necessary for this program to represent an NxN matrix as a ROWSx2 matrix
def getNumMatrixRows(sideLength):
    return ((sideLength * sideLength - sideLength) / 2)

def getWeights(thePairs):
    weightInfo = []
    for i, pair in enumerate(thePairs):
        weightResult = calcWeight(pair)
        weightInfo.append([i, weightResult[0], weightResult[1]])
    return sorted(weightInfo, key=lambda weightInfo: weightInfo[2], reverse=True)

def calcWeight(pairIn):
    trueVotes = int(pairIn[0])
    falseVotes = int(pairIn[1])
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

    return [isTrue, weight]

main()