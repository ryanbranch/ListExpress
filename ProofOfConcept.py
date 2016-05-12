#!/usr/bin/env python

"""ProofOfConcept.py: Used to search for flaws in the ListExpress algorithm"""

import random
import csv
import math
import scipy.stats

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
        self.relationTrue = boolIn
    #Get function for relationTrue
    def getRelationTrue(self):
        return self.relationTrue

class Test:
    #Default constructor
    def __init__(self):
        self.numElts = 0
        self.comparisons = []
        self.hasse = []

        #relationList is a list of 2-elt tuples, where the tuple represents 2 items being compared
        self.relationList = []
        #relationDict is a dictionary where the keys are 2-elt tuples as in relationList
        #Definitions are signed weights which are positive if the tuple correctly describes the greater/lesser order
        self.relationDict = {}

        #Stores the sum of all UNSIGNED weights calculated
        self.totalAllWeights = 0

    #Populates the relation list based on number of elements (Forward direction).
    def buildRelationList(self):
        for i in range(self.numElts - 1):
            for j in range(i + 1, self.numElts):
                self.relationList.append((i,j))
        print(str(self.relationList) + "\n")

    #Creates and populates the relation dictionary based on the unsorted list of comparisons
    def buildRelationDict(self):
        for i, comp in enumerate(self.comparisons):
            newWeight = comp.getWeight()
            self.totalAllWeights += newWeight

            #Accounts for the order of the relation
            if (comp.getGreater > comp.getLesser):
                newWeight *= -1

            #Accounts for the truth of the relation
            if not comp.getRelationTrue():
                newWeight *= -1

            #Adds to the dictionary
            self.relationDict[self.relationList[i]] = newWeight

    #Creates the most satisfiable hasse diagram from the given comparison data
    #The list is built in descending order
    def buildHasse(self):

        #First, adds the 2 items in the highest weighted comparison, since those are guaranteed
        self.hasse = [self.comparisons[0].getGreater(), self.comparisons[0].getLesser()]
        self.comparisons[0].setImplemented(True)

        #Iterates through the comparisons starting with the 2nd element, then the 3rd, then the 2nd, 3rd, 4th... etc
        for i in range(1, getNumMatrixRows(self.numElts)):
            for j in range(1, i + 1):

                #If the comparison at j has not yet been implemented, we attempt to do so
                if not self.comparisons[j].getImplemented():
                    gNum = self.comparisons[j].getGreater()
                    lNum = self.comparisons[j].getLesser()

                    #We can only use a comparison if one of its elements are in the diagram
                    gIn = gNum in self.hasse
                    lIn = lNum in self.hasse
                    if (gIn != lIn):

                        #The if and elif statements below have 2 different processing methods that I'm currently testing
                        #NOTE: The second goes through everything, the first is more range limited.

                        #so far they're returing almost identical totals at the end. keeping first is BARELY better than second?

                        #lNum is not yet in the diagram
                        if (gIn and not lIn):
                            #self.insertHasse(lNum, (gNum + 1), len(self.hasse), (j + 1))
                            self.insertHasse(lNum, 0, len(self.hasse), (j + 1))

                        #gNum is not yet in the diagram
                        elif (lIn and not gIn):
                            #self.insertHasse(gNum, 0, self.hasse.index(lNum), (j + 1))
                            self.insertHasse(gNum, 0, len(self.hasse), (j + 1))

                        #Updates the implemented variable for this comparison
                        self.comparisons[i].setImplemented(True)

    #Finds the best index at the list to insert the new item
    #newElt is the value of the new list element to be inserted
    #upperIdx is the highest value (lowest index) space the element is allowed to occupy
    #lowerIdx is the lowest value (highest index) space the element is allowed to occupy
    #condIdx is the index of the first condition to apply in self.comparisons
    def insertHasse(self, newElt, upperIdx, lowerIdx, condIdx):

        print("Inserting " + str(newElt) + " into self.hasse")
        print("Before: " + str(self.hasse))

        #This dictionary stores weight sum data, using the insertion index of newElt as the key
        weightSumDict = {}

        #Calculates the initial weight sum which is used to streamline the process of calculating the rest
        #The initial weight sum is the sum of satisfied condition weights when newElt is inserted at upperIdx
        tempHasse = self.hasse[:]
        tempHasse.insert(upperIdx, newElt)
        currentSum = self.sumWeights(tempHasse)
        weightSumDict[upperIdx] = currentSum

        #Saves some initial information for finding the max later
        maxWeight = currentSum
        maxIdx = upperIdx

        #Iterates through each possible insertion point, calculating and recording the weight sum
        for i in range(upperIdx + 1, lowerIdx + 1):

            #To modify the currentSum, we use the comparison between newElt and the elt at index (i - 1)
            currentSum += (2 * self.getWeightFor(self.hasse[i - 1], newElt))
            weightSumDict[i] = currentSum
        print(weightSumDict)

        #Now that weightSumDict has been built, newElt should be added to self.hasse
        #It is added at the index of the weightSumDict key corresponds to the highest weight
        for indexKey, weight in weightSumDict.iteritems():
            if weight > maxWeight:
                maxIdx = indexKey
                maxWeight = weight
        self.hasse.insert(maxIdx, newElt)
        print("maxIdx: " + str(maxIdx))

        print("After: " + str(self.hasse) + "\n")

        return

    #Determines the sum of weights of comparisons satisfied by a given hasse list
    def sumWeights(self, testHasse):
        theSum = 0
        for comp in self.comparisons:
            gItem = comp.getGreater()
            lItem = comp.getLesser()

            if ((gItem in testHasse) and (lItem in testHasse)):
                gIdx = testHasse.index(gItem)
                lIdx = testHasse.index(lItem)

                #If testHasse satisfies the condition, add the weight.  Otherwise, subtract it
                if gIdx < lIdx:
                    theSum += comp.getWeight()
                else:
                    theSum -= comp.getWeight()
        return theSum

    #Returns the signed weight of the comparison between first and second.
    #If the first item is greater than the second, returns a positive number.  Else, returns a negative.
    def getWeightFor(self, first, second):
        if first < second:
            print("WEIGHT: " + str(self.relationDict[(first, second)]))
            return self.relationDict[(first, second)]
        elif second < first:
            return (-1 * self.relationDict[(second, first)])
        else:
            print("ERROR: first == second")
            exit()

    #Set function for numElts
    def setNumElts(self, numIn):
        self.numElts = numIn
    #Get function for numElts
    def getNumElts(self):
        return self.numElts

    #Set function for relationList
    def setRelationList(self, listIn):
        self.relationList = listIn
    #Get function for relationList
    def getRelationList(self):
        return self.relationList

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

    #Set function for totalAllWeights
    def setTotalAllWeights(self, numIn):
        self.totalAllWeights = numIn
    #Get function for totalAllWeights
    def getTotalAllWeights(self):
        return self.totalAllWeights

def main():
    random.seed("0")
    theTest = Test()
    fileIn(theTest)
    theTest.buildRelationList()

    #Iterates through the dictionary and updates each Comparison with its "definition"
    for i, pair in enumerate(theTest.getRelationList()):
        if (((theTest.getComparisons())[i]).getRelationTrue()):
            greaterVal = pair[0]
            lesserVal = pair[1]
        else:
            greaterVal = pair[1]
            lesserVal = pair[0]
        theTest.getComparisons()[i].setGreater(greaterVal)
        theTest.getComparisons()[i].setLesser(lesserVal)

    #Sorts the comparison list, printing some of the information before and after
    theTest.printComparisons()

    #Before sorting comparisons, builds relationDict
    theTest.buildRelationDict()

    #Sorts the comparisons by weight
    theTest.setComparisons(sorted(theTest.getComparisons(), key=lambda comp: comp.getWeight(), reverse=True))
    theTest.printComparisons()

    theTest.buildHasse()
    print("FINAL HASSE:")
    print(theTest.hasse)

    #Calculates theSum without subtractions as the average of (that with subtractions and theTotal)
    theTotal = theTest.getTotalAllWeights()
    theSum = (theTotal + (theTest.sumWeights(theTest.hasse))) / 2

    print("SUM OF WEIGHTS:")
    print(theSum)
    print("TOTAL ALL WEIGHTS:")
    print(theTotal)
    print("SATISFACTION RATIO")
    print(str(theSum / theTotal))

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
            test.addComparison(Comparison(int(row[1]), int(row[0]), (rowNum - 2)))
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