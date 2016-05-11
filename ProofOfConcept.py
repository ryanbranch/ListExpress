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

class Test:
    #MEMBER VARIABLES:
    #Placeholder

    #Default constructor
    def __init__(self):
        self.numElts = 0
        self.pairs = []

    #Creates and populates the relation dictionary based on number of elements (Forward direction).
    def buildDict(self):
        self.relationDict = {}
        theTot = 0
        for i in range(self.numElts - 1):
            for j in range(i + 1, self.numElts):
                #print str(theTot) + " \t" + str(i) + " \t" + str(j)
                self.relationDict[theTot] = (i,j)
                theTot += 1
        #print("\n")

    def buildSet(self, theWeights):
        #Defines an instance of the Sudoku object for the class to use
        self.sudoku = Sudoku(self.numElts)

        #Goes through the voted conditions once and builds the set accordingly
        for i, weight in enumerate(theWeights):
            #defines voteInfo, a tuple describing inequality between two items
            #The first element is the greater item, the second element is the lesser one
            voteInfo = self.relationDict[weight[0]]
            if weight[1]:
                self.sudoku.oneStep(voteInfo[0], voteInfo[1])
            else:
                self.sudoku.oneStep(voteInfo[1], voteInfo[0])
            print(str(self.sudoku.getBoxes()) + "\n\n")

        #If there is more specification to be done, then do so
        remaining = self.sudoku.getItemsLeft()
        print("REMAINING: " + str(remaining))
        keyNum = 0
        while remaining:
            votePair = self.relationDict[keyNum]

            #If both items in the pair are remaining,
            if ((votePair[0] in remaining) and (votePair[1] in remaining)):
                #print("Running comparison on " + str(votePair) + " AGAIN.")
                if theWeights[keyNum][1]:
                    self.sudoku.oneStep(votePair[0], votePair[1])
                else:
                    self.sudoku.oneStep(votePair[1], votePair[0])
                print("\n")

            #Increments keyNum, wrapping around each time it reaches the end of the dictionary
            if (keyNum >= (getNumMatrixRows(self.numElts) - 1)):
                keyNum = 0
            else:
                keyNum += 1

            #Updates the value of remaining
            remaining = self.sudoku.getItemsLeft()
        print("\n")

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
        self.itemsSeen = []
        self.allSeen = False
        self.dontClean = []

        #Initializes itemsLeft as the number of items in the system
        #As positions are confirmed, the items are removed from this list
        self.itemsLeft = []
        for i in range(self.numBoxes):
            self.itemsLeft.append(i)

        for i in range(self.numBoxes):
            self.boxes.append([])

    #Gets one step closer to figuring out the final order each time it's run with a given input
    #Self.boxes is a list in descending order.  So self.boxes[0] is the highest ranked spot
    #As a general rule, if the program hasn't seen an item yet, it will add it to one or more boxes during this function
    #If it has seen the item, it will remove it from zero or more boxes during this function.
    def oneStep(self, greater, lesser):
        print("Choice " + str(greater) + " \t> \tChoice " + str(lesser))

        #If either greater or lesser has yet to be finished, we do that
        if ((lesser in self.itemsLeft) or (greater in self.itemsLeft)):
            print("Pre-operation boxes: " + str(self.boxes))

            if not self.allSeen:
                gSeen = (greater in self.itemsSeen)
                lSeen = (lesser in self.itemsSeen)
            else:
                gSeen = True
                lSeen = True

            somethingNew = False
            somethingRemoved = False
            allSeenUpdated = False

            setBounds = False

            #One way a condition is invalid is if the highest instance of greater is below the lowest of lesser.
            if self.allSeen:
                print(self.itemsSeen)
                highestG = self.getHighestGreater(greater)
                lowestL = self.getLowestLesser(lesser)
                print("highestG: " + str(highestG) + ", lowestL: " + str(lowestL))
                setBounds = True
                #The truth of this boolean defines an invalid attempt, so we return early
                #An attempt is invalid if highestG doesn't exist in a greater position than lowestL
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
                    #Finally, this does not apply if that box only contains 1 element.
                    if lesser in self.itemsLeft:
                        i = self.numBoxes - 1
                        while ((len(self.boxes[i]) == 1) and (self.boxes[i][0] not in self.itemsLeft)):
                            i -= 1

                        #The condition is invalid if the box only has 1 element, so we return early
                        if len(self.boxes[i]) == 1:
                            return

                        #Otherwise, removes the item from that box
                        #Note: This could potentially go out of bounds for a completed list
                        elif greater in self.boxes[i]:
                            self.boxes[i].remove(greater)

                            #This should be done whenever something is removed from self.boxes
                            somethingRemoved = True

                if lSeen:
                    #Removes the lesser item from any boxes at or higher than highestG
                    #The removal of lesser can make oneStep's condition potentially invalid:
                    #If removing  lesser from boxes would leave 2 or more boxes which contained a single instance
                    #of the same item, then the condition of this whole function is invalid and nothing should be done
                    #Also, if removing lesser would leave any empty boxes, the situation is invalid as well
                    #NOTE: This is a generator expression. It seems super useful and I should learn this better
                    #This iterates through selection, which is generated on the fly as a list of all the elements in
                    #self.boxes where that element (which is a list) contains lesser and is in the "danger zone"
                    invalidRemoval = False
                    matches = []

                    #Checks the length 1 condition (no leaving empty boxes allowed)
                    for selection in (box for box in self.boxes if (len(box) == 1)):
                        if selection[0] == lesser:
                            invalidRemoval = True

                    #If we didn't just find that removal invalid, need to check the length 2 condition
                    if not invalidRemoval:

                        #Finds every box that contains lesser and is in the "danger zone" for removal and is of length 2
                        for selection in (box for i, box in enumerate(self.boxes) if
                                          ((i <= highestG) and (lesser in box) and (len(box) == 2))):
                            if selection[0] == lesser:
                                if selection[0] in matches:
                                    invalidRemoval = True
                                else:
                                    matches.append(selection[0])
                            else:
                                if selection[1] in matches:
                                    invalidRemoval = True
                                else:
                                    matches.append(selection[1])

                    if not invalidRemoval:
                        for i in range(highestG + 1):
                            if lesser in self.boxes[i]:
                                self.boxes[i].remove(lesser)

                                #This should be done whenever something is removed from self.boxes
                                somethingRemoved = True
                    else:
                        print("INVALID REMOVAL ATTEMPT")
                        return

                else:
                    for i in range(highestG + 1, self.numBoxes):
                        self.boxes[i].append(lesser)
                    self.itemsSeen.append(lesser)

                    #This should be done whenever something is appended to itemsSeen
                    somethingNew = True

            #If the lesser value has been processed before
            if lSeen:
                print("LSEEN")

                #Calculates the value of the lowest ranked box which contains "lesser"
                if not setBounds:
                    lowestL = self.getLowestLesser(lesser)

                #We know that lesser is lower rank than greater, so it can't exist in the highest unfilled spot
                #This also only applies when greater is in self.itemsLeft
                if greater in self.itemsLeft:
                    i = 0
                    while ((len(self.boxes[i]) == 1) and (self.boxes[i][0] not in self.itemsLeft)):
                        i += 1
                    #Note: This could potentially go out of bounds for a completed list
                    if lesser in self.boxes[i]:
                        self.boxes[i].remove(lesser)

                        #This should be done whenever something is removed from self.boxes
                        somethingRemoved = True

                if gSeen:
                    #Removes the greater item from any boxes at or below lowestL
                    #The removal of greater can make oneStep's condition potentially invalid:
                    #If removing  greater from boxes would leave 2 or more boxes which contained a single instance
                    #of the same item, then the condition of this whole function is invalid and nothing should be done
                    #Also, if removing lesser would leave any empty boxes, the situation is invalid as well
                    invalidRemoval = False
                    matches = []

                    #Checks the length 1 condition (no leaving empty boxes allowed)
                    for selection in (box for box in self.boxes if (len(box) == 1)):
                        if selection[0] == lesser:
                            invalidRemoval = True

                    #If we didn't just find that removal invalid, need to check the length 2 condition
                    if not invalidRemoval:

                        #Finds every box that contains greater and is in the "danger zone" for removal and is of length 2
                        for selection in (box for i, box in enumerate(self.boxes) if
                                          ((lowestL <= i < self.numBoxes) and(greater in box) and (len(box) == 2))):
                            if selection[0] == greater:
                                if selection[0] in matches:
                                    invalidRemoval = True
                                else:
                                    matches.append(selection[0])
                            else:
                                if selection[1] in matches:
                                    invalidRemoval = True
                                else:
                                    matches.append(selection[1])

                    if not invalidRemoval:
                        for i in range(lowestL, self.numBoxes):
                            if greater in self.boxes[i]:
                                self.boxes[i].remove(greater)

                                #This should be done whenever something is removed from self.boxes
                                somethingRemoved = True
                    else:
                        print("INVALID REMOVAL ATTEMPT")
                        return

                else:
                    for i in range(lowestL - 1, -1, -1):
                        self.boxes[i].append(greater)
                    self.itemsSeen.append(greater)

                    #This should be done whenever something is appended to itemsSeen
                    somethingNew = True

            #If neither of the values have been processed before
            if ((not gSeen) and (not lSeen)):
                for i in range(self.numBoxes - 1):
                    (self.boxes[i]).append(greater)
                    (self.boxes[i+1]).append(lesser)
                (self.itemsSeen).append(greater)
                (self.itemsSeen).append(lesser)

                #This should be done whenever something is appended to itemsSeen
                somethingNew = True

            #If we just saw something new, check if we've seen everything
            if ((self.allSeen == False) and (somethingNew)):
                self.allSeen = ((len(self.itemsSeen)) == (self.numBoxes))
                allSeenUpdated = self.allSeen

            #If all numbers have been seen and something was removed from self.boxes, we attempt to clean up
            #Turns out somethingRemoved is not a requirement for cleanup.  For example if 4 of 5 items already exist
            #In the list, there are situations where the 5th one can be added and a box will end up with only 1 item.
            if ((self.allSeen) and ((somethingRemoved) or (allSeenUpdated))):
                print("Attempting to clean up the boxes")
                self.cleanup()

                #NOTE: dontClean should always be reset after cleanup.
                dontClean = []

        else:
            print("Condition complete. No need for modification.")

    def cleanup(self):
        print("Pre-cleanup boxes: " + str(self.boxes))
        leftInit = len(self.itemsLeft)

        uniqueItem = -1
        uniqueIndex = -1

        #Locates and saves the position of any item that exists alone in a box
        for i, box in enumerate(self.boxes):
            if ((len(box) == 1) and (box[0] in self.itemsLeft) and (box[0] not in self.dontClean)):
                uniqueItem = box[0]
                uniqueIndex = i

        #The removal of uniqueItem can make cleanup's condition potentially invalid:
        #If removing  uniqueItem from boxes would leave 2 or more boxes which contained a single instance
        #of the same item, then uniqueItem isn't removed, but instead added to a list to keep track of it
        invalidRemoval = False
        matches = []

        #Finds every box which contains uniqueItem and one other item. Stores in matches.
        for selection in (box for i, box in enumerate(self.boxes) if ((len(box) == 2) and (uniqueItem in box))):
            if selection[1] == uniqueItem:
                if selection[0] in matches:
                    invalidRemoval = True
                else:
                    matches.append(selection[0])
            else:
                if selection[1] in matches:
                    invalidRemoval = True
                else:
                    matches.append(selection[1])

        #If the removal of uniqueItem is invalid, adds uniqueItem to dontClean for these rounds.
        if(invalidRemoval):
            self.dontClean.append(uniqueItem)
        else:

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
        appearances = self.getFrequencies()

        #Locks in the position of any item that only exists once throughout all of boxes
        for i in range(self.numBoxes):
            if appearances[i][1] == 1:
                self.boxes[appearances[i][0]] = [i]
                self.itemsLeft.remove(i)
                print ("Removed " + str(i) + " from self.itemsLeft")

        #If any progress was made throughout this function, we rerun the function until no progress is made
        if len(self.itemsLeft) != leftInit:
            print("Running cleanup AGAIN!")
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
        while ((lowL == -1) and (i >= 0)):
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

    #Returns a dictionary with a key for each box.  The keys correspond to lists of length 2.
    #Each list contains: The last (lowest) box the item is in, and the total frequency with which it
    #appears over all of the boxes
    #Note: Since the first list element (position) for each item is initialized as -1, one should always
    #ensure that this element is nonnegative, as long as the second element is nonzero.
    #Just be careful when working with this data.
    def getFrequencies(self):
        freqs = {}

        #Initializes the empty dictionary to count instances of each item
        for i in range(self.numBoxes):
            freqs[i] = [-1,0]

        #Replaces the appropriate values within the lists in freqs to keep track of information
        for i, box in enumerate(self.boxes):
            for j in self.itemsLeft:
                if j in box:
                    freqs[j][0] = i
                    freqs[j][1] += 1

        return freqs

    #Set function for boxes
    def setBoxes(self, boxesIn):
        self.boxes = boxesIn
    #Get function for boxes
    def getBoxes(self):
        return self.boxes

    #Set function for itemsLeft
    def setItemsLeft(self, itemsIn):
        self.itemsLeft = itemsIn
    #Get function for itemsLeft
    def getItemsLeft(self):
        return self.itemsLeft

def main():
    random.seed("0")
    theTest = Test()
    fileIn(theTest)

    #NOTE: WeightList etc. are bad names for these because it's not just a list of weights but a 2d list where the inner list contains weight, among other things.
    #In the future, I can possibly shave down weightlist to not include these weightings used for ordering.  Not quite sure yet.
    weightList = getWeights(theTest.getPairs())

    #Prints some diagnostic output useful for viewing test results.  Will remove eventually
    for elt in weightList:
        print str(elt[0]) + ". " + str(elt[1]) + "  \t" + str(theTest.getPairs()[elt[0]]) + "  \t" + str(elt[2])

    theTest.buildDict()
    print("|================================|\n")

    #Orders the elements based on now-ordered list of weighted comparisons
    theTest.buildSet(weightList)
    print("Done!  Final ordered list:")
    print(str(theTest.sudoku.getBoxes()))

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

        #NOTE: The code to populate self.pairs in either mode assumes perfectly formatted data.
        #Populates self.pairs for manual mode
        else:
            pair = [int(row[1]), int(row[0])]
            test.addPair(pair)
        rowNum += 1

        #Populates self.pairs for random mode
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
    weight = 0

    #As long as both the true and false votes are not zero, weight is nonzero
    if total != 0:
       deviation  = (theMax / total) - 0.5

       #math.log is base e (ln)
       weight = deviation * math.log(total)

    return [isTrue, weight]

main()