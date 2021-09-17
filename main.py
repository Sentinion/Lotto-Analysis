#other importing
import requests
import pandas
import time
from bs4 import BeautifulSoup
from random import Random, sample, randrange, choice, randint
import numpy as np


#Here the user can input all the stocks they want to check
yearsToCheck = ["2020", "2019", "2018", "2017", "2016"]

#Will return a DF containing all the numbers From December 25 2020 to September 6 1996
def get_testing_numbers():
    '''
    Want to keep results per year for each year 
    Previous performance was measured in interval of 5 years so will be 1996 - 2000, 2001-2005, 2006-2010, 2011-2015, 2016-2020 (25 years in total including the training ranges to verify we are running the right simulation as the first time)
    Hoping that we find consistent results using the optimal range of lotto numbers between each yearly set of 5 E.g. approx 386 wins with range and 11 for rand
    MAKE SURE TO USE BULKFASTCHECKER and bulksim so that we test the same number of iterations
    Should pull in historical data to excel initially because it should be much faster to read (should be about 2000 entries) and will allow for further statistical analysis of # distributions if we find that our wins per 5 years isn't consistent over time
    Should change the bulkfastchecker to print to a file so that results can be viewed showing at the end:


    Total number of simulations
    Total number of drawings
    
    for each yearly range:
        Total wins for range
        Total wins for rand

    Total Wins from range over all 20 years
    Total Wins from rand over all 20 years


    '''
    historicDF = pandas.DataFrame(columns=["Draw Date", "#1", "#2", "#3", "#4", "#5", "#6"])

    #Taking care of first page that includes starting date because it will avoid an if statement each time in the loop
    url = "https://www.usamega.com/mega-millions/results/3"
    try:
            page = requests.get(url)
            tasty_data_soup = BeautifulSoup(page.content, 'html.parser')
            #Need to get the lotto
            '''
            For website lotto results are in in tbody > tr > THE FIRST td > section class results > ul
            Date is in tbody > tr > THE FIRST td > section class results > a (Will need to split by comma, strip each component, ignore first elem which is dow, then format as mm/dd/yyyy)
            '''
            tableBody = tasty_data_soup.find("table", {"class": "lottery-table"}) 
            tableRows = tableBody.find_all("tr")
            indeces = []
            numbers = []
            for row in tableRows[2:]:
                rowParts = row.get_text().splitlines()
                date = rowParts[2]
                indeces.append(date)
                winningNumbers = rowParts[4].split("-")[:6]
                #print(date + ", " + str(winningNumbers))
                numbers.append(winningNumbers)
            
            pageDF = pandas.DataFrame(columns=["#1", "#2", "#3", "#4", "#5", "#6"], index=indeces)
            iterator = 0
            while iterator < len(numbers):
                winningNums = numbers[iterator]
                yearlyDF.iloc[iterator] = [winningNums[0], winningNums[1], winningNums[2], winningNums[3], winningNums[4], winningNums[5]]
                iterator+=1
    except:
        print("Failed to access website given url: " + url)

    for i in range(4,99):
        url = "https://www.usamega.com/mega-millions/results/" + str(i)

        #Want to start at December 25th to include the correct date
        try:
            page = requests.get(url)
            tasty_data_soup = BeautifulSoup(page.content, 'html.parser')
            #Need to get the lotto
            tableBody = tasty_data_soup.find("table", {"class": "lottery-table"})
            tableRows = tableBody.find_all("tr")
            indeces = []
            numbers = []
            for row in tableRows[2:]:
                rowParts = row.get_text().splitlines()
                date = rowParts[2]
                indeces.append(date)
                winningNumbers = rowParts[4].split("-")[:6]
                #print(date + ", " + str(winningNumbers))
                numbers.append(winningNumbers)
            
            pageDF = pandas.DataFrame(columns=["#1", "#2", "#3", "#4", "#5", "#6"], index=indeces)
            iterator = 0
            while iterator < len(numbers):
                winningNums = numbers[iterator]
                yearlyDF.iloc[iterator] = [winningNums[0], winningNums[1], winningNums[2], winningNums[3], winningNums[4], winningNums[5]]
                iterator+=1
        except:
            print("Failed to access website given url: " + url)
    # https://www.usamega.com/mega-millions/results/98 results go from / to /98 which goes till the year 1996
    pass



def get_winning_numbers(year):
    url = "https://lottery.com/previous-results/or/megamillions/" + year
    yearlyDF = pandas.DataFrame(columns=["Draw Date", "#1", "#2", "#3", "#4", "#5", "#6"])

    try:
        page = requests.get(url)
        tasty_data_soup = BeautifulSoup(page.content, 'html.parser')
        #Need to get the lotto
        tableBody = tasty_data_soup.find("table", {"class": "lottery-table"})
        tableRows = tableBody.find_all("tr")
        indeces = []
        numbers = []
        for row in tableRows[2:]:
            rowParts = row.get_text().splitlines()
            date = rowParts[2]
            indeces.append(date)
            winningNumbers = rowParts[4].split("-")[:6]
            #print(date + ", " + str(winningNumbers))
            numbers.append(winningNumbers)
        
        yearlyDF = pandas.DataFrame(columns=["#1", "#2", "#3", "#4", "#5", "#6"], index=indeces)
        iterator = 0
        while iterator < len(numbers):
            winningNums = numbers[iterator]
            yearlyDF.iloc[iterator] = [winningNums[0], winningNums[1], winningNums[2], winningNums[3], winningNums[4], winningNums[5]]
            iterator+=1
        return yearlyDF

    except:
        print("Failed to access website")


mainDF = pandas.DataFrame(columns=["#1", "#2", "#3", "#4", "#5", "#6"])
for year in yearsToCheck:
   mainDF = pandas.concat([mainDF, get_winning_numbers(year)])

'''
print(mainDF)
mainDF.to_excel("LottoData.xlsx")
'''

#This function was created to test stricter and more leniant ranges to try and find the most optimal range to generate lotto numbers from
def rangesRandomChecker(numIterations):
    timeToRunStart = time.perf_counter()

    numLessRangeWins = 0
    numBaseRangeWins = 0
    numMoreRangeWins = 0

    rangesDict = {
        #"less_strict": [[1,2,3,4,6,7,8,10,11], [13,15,16,17,20,22,24,33], [24,28,30,31,32,34,37,39,41,42,44,53], [42,43,48,49,54,56,61], [58,60,62,64,66,67,68,69,70], [1,6,7,9,10,11,13,14,22]], #FIRST
        # "less_strict": [[1,2,3,4,7,8,10,11], [13,16,17,20,22,24,33], [30,31,34,37,39,41,44,53], [42,43,48,49,54,56], [62,64,66,67,68,70], [1,6,7,9,10,11,13,14,22]], #SECOND
        # "starting": [[1,2,3,4,7,8,10,11], [13,16,17,20,22,24,33], [30,31,34,37,39,41,44,53], [42,43,48,49,54,56], [62,64,66,67,68,70], [6,9,10,11,14,22]], #FIRST
        # "stricter": [[1,2,3,4,7,8,10,11], [13,16,17,20,22,24,33], [30,31,34,37,39,41,44,53], [42,43,48,49,54,56], [62,64,66,67,68,70], [9,10,11,22]] #SECOND
        #"stricter": [[1,2,3,4,7,8], [17,22,24], [31,34,37,39], [42,48,54,56], [62,64,68,70], [9,10,11,22]] #FIRST
        "less_strict": [[1,2,3,4,6,7,8,10,11], [13,16,17,20,22,24,33], [30,31,34,37,39,41,44,53], [42,43,48,49,54,56], [62,64,66,67,68,70], [9,10,11,22]], #FOURTH
        "starting": [[1,2,3,4,7,8,10,11], [13,16,17,20,22,24,33], [30,31,34,37,39,41,44,53], [42,43,48,49,54,56], [62,64,66,67,68,70], [9,10,11,22]], #FOURTH
        "stricter": [[1,2,3,4,7,8], [13,16,17,20,22,24,33], [30,31,34,37,39,41,44,53], [42,43,48,49,54,56], [62,64,66,67,68,70], [9,10,11,22]] #FOURTH
    }

    #DIFFERENT RANGE BALL GENERATION
    timeBeforeRangeGen = time.perf_counter()
    lessBall1 = np.random.choice(rangesDict["less_strict"][0], size=numIterations*395)
    lessBall2 = np.random.choice(rangesDict["less_strict"][1], size=numIterations*395)
    lessBall3 = np.random.choice(rangesDict["less_strict"][2], size=numIterations*395)
    lessBall4 = np.random.choice(rangesDict["less_strict"][3], size=numIterations*395)
    lessBall5 = np.random.choice(rangesDict["less_strict"][4], size=numIterations*395)
    lessBall6 = np.random.choice(rangesDict["less_strict"][5], size=numIterations*395)
    timeAfterRangeGen = time.perf_counter()
    timeToRangeGen = timeAfterRangeGen-timeBeforeRangeGen
    print("Total time to generate " + str(numIterations*395*6) + " less strict random numbers with Numpy: " + str(timeToRangeGen))

    timeBeforeRangeGen = time.perf_counter()
    baseBall1 = np.random.choice(rangesDict["starting"][0], size=numIterations*395)
    baseBall2 = np.random.choice(rangesDict["starting"][1], size=numIterations*395)
    baseBall3 = np.random.choice(rangesDict["starting"][2], size=numIterations*395)
    baseBall4 = np.random.choice(rangesDict["starting"][3], size=numIterations*395)
    baseBall5 = np.random.choice(rangesDict["starting"][4], size=numIterations*395)
    baseBall6 = np.random.choice(rangesDict["starting"][5], size=numIterations*395)
    timeAfterRangeGen = time.perf_counter()
    timeToRangeGen = timeAfterRangeGen-timeBeforeRangeGen
    print("Total time to generate " + str(numIterations*395*6) + " base strict random numbers with Numpy: " + str(timeToRangeGen))

    timeBeforeRangeGen = time.perf_counter()
    moreBall1 = np.random.choice(rangesDict["stricter"][0], size=numIterations*395)
    moreBall2 = np.random.choice(rangesDict["stricter"][1], size=numIterations*395)
    moreBall3 = np.random.choice(rangesDict["stricter"][2], size=numIterations*395)
    moreBall4 = np.random.choice(rangesDict["stricter"][3], size=numIterations*395)
    moreBall5 = np.random.choice(rangesDict["stricter"][4], size=numIterations*395)
    moreBall6 = np.random.choice(rangesDict["stricter"][5], size=numIterations*395)
    timeAfterRangeGen = time.perf_counter()
    timeToRangeGen = timeAfterRangeGen-timeBeforeRangeGen
    print("Total time to generate " + str(numIterations*395*6) + " more strict random numbers with Numpy: " + str(timeToRangeGen))

    #print("Finished Num Generation")
    rangeIndex = 0
    for index, row in mainDF.iterrows():
        drawingDayNumbers = [int(row["#1"]), int(row["#2"]), int(row["#3"]), int(row["#4"]), int(row["#5"]), int(row["#6"])]

        #Range Random Number Comparison
        for i in range(numIterations):
            #LESS COMBINATION
            sortedLessNums = [lessBall1[rangeIndex], lessBall2[rangeIndex], lessBall3[rangeIndex], lessBall4[rangeIndex], lessBall5[rangeIndex]]
            sortedLessNums.sort()
            sortedLessNums.append(lessBall6[rangeIndex])

            #BASE COMBINATION
            sortedBaseNums = [baseBall1[rangeIndex], baseBall2[rangeIndex], baseBall3[rangeIndex], baseBall4[rangeIndex], baseBall5[rangeIndex]]
            sortedBaseNums.sort()
            sortedBaseNums.append(baseBall6[rangeIndex])

            #MORE COMBINATION
            sortedMoreNums = [moreBall1[rangeIndex], moreBall2[rangeIndex], moreBall3[rangeIndex], moreBall4[rangeIndex], moreBall5[rangeIndex]]
            sortedMoreNums.sort()
            sortedMoreNums.append(moreBall6[rangeIndex])

            if sortedLessNums == drawingDayNumbers:
                numLessRangeWins+=1

            if sortedBaseNums == drawingDayNumbers:
                numBaseRangeWins+=1

            if sortedMoreNums == drawingDayNumbers:
                numMoreRangeWins+=1
            
            rangeIndex += 1
    timeToRunEnd = time.perf_counter()

    print("Num wins out of " + str(numIterations) + " simulations, testing " + str(numIterations*395*6) + " numbers, in " + str(numIterations*395) + " drawings with less strict range randomness: " + str(numLessRangeWins))
    print("Num wins out of " + str(numIterations) + " simulations, testing " + str(numIterations*395*6) + " numbers, in " + str(numIterations*395) + " drawings with base range randomness: " + str(numBaseRangeWins))
    print("Num wins out of " + str(numIterations) + " simulations, testing " + str(numIterations*395*6) + " numbers, in " + str(numIterations*395) + " drawings with more strict range randomness: " + str(numMoreRangeWins))
    print("Ran in " + str(timeToRunEnd-timeToRunStart) + " seconds")
    return [numLessRangeWins, numBaseRangeWins, numMoreRangeWins]

#This function allows the user to check the number of lottery numbers generated with duplicates. I used this to see if the reason I wasn't winning as many purely random sets was because of an abundance of duplicaates but I concluded that wasn't the case
def singleDrawingChecker(numIterations):
    timeToRunStart = time.perf_counter()
    numTrueWins = 0
    numRangeWins = 0

    dfAccessTimes = [] 

    #True Random Selection Section
    timeBeforeRandGen = time.perf_counter()
    true_whiteBalls = np.random.randint(70, size=numIterations*395*5) #Because these are ndarrays, access elements in them like an array DONT DELETE IT MAKES NEW OBJECTS WHICH SLOWS PROGRAM
    true_megaBalls =  np.random.randint(25, size=numIterations*395)

    timeAfterRandGen = time.perf_counter()
    timeToRandGen = timeAfterRandGen-timeBeforeRandGen

    print("Total time to generate " + str(numIterations*395*6) + " true random numbers with Numpy: " + str(timeToRandGen))

    #Range Random Selection Section
    timeBeforeRangeGen = time.perf_counter()
    whiteBall1 = np.random.choice([1,2,3,4,7,8,10,11], size=numIterations*395)
    whiteBall2 = np.random.choice([13,16,17,22,24,33], size=numIterations*395)
    whiteBall3 = np.random.choice([31,34,35,39,41,44,53], size=numIterations*395)
    whiteBall4 = np.random.choice([42,43,46,48,49,54,56,61], size=numIterations*395)
    whiteBall5 = np.random.choice([58,60,62,64,66,67,68,69,70], size=numIterations*395)
    range_megaBall = np.random.choice([6,9,10,11,14,22], size=numIterations*395)

    whiteBallsIndex = 0
    megaBallsIndex = 0
    rangeIndex = 0

    row = mainDF.iloc[0]

    drawingDayNumbers = [int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5])]
    totalWhiteBallsGenerated = len(true_whiteBalls)
    uniqueWhiteBallsCompared = 0
    totalRangeBallsGenerated = len(whiteBall1*5)
    uniqueRangeBallsCompared = 0
    #True Random Number Comparison
    while whiteBallsIndex < len(true_whiteBalls)-4:
        sortedNums = [true_whiteBalls[whiteBallsIndex], true_whiteBalls[whiteBallsIndex+1], true_whiteBalls[whiteBallsIndex+2], true_whiteBalls[whiteBallsIndex+3], true_whiteBalls[whiteBallsIndex+4]]
        sortedNums.sort()
        sortedNums.append(true_megaBalls[megaBallsIndex])
        if len(set(sortedNums)) == len(sortedNums):
            if sortedNums == drawingDayNumbers:
                numTrueWins += 1
            uniqueWhiteBallsCompared += 5
            #print("TRUE WINS --- CURRENT TRUE WINS: " + str(numTrueWins))
        #print("Comparison #" + str(i) + "completed")
        whiteBallsIndex += 5
        megaBallsIndex += 1
        
    #Range Random Number Comparison
    while rangeIndex < len(whiteBall1):
        sortedNums = [whiteBall1[rangeIndex], whiteBall2[rangeIndex], whiteBall3[rangeIndex], whiteBall4[rangeIndex], whiteBall5[rangeIndex]]
        sortedNums.sort()
        sortedNums.append(range_megaBall[rangeIndex])
        if len(set(sortedNums)) == len(sortedNums):
            if sortedNums == drawingDayNumbers:
                numRangeWins+=1
            uniqueRangeBallsCompared += 1
            #print("RANGE WINS --- CURRENT RANGE WINS: " + str(numRangeWins))
        rangeIndex += 1

    print("Num wins out of " + str(numIterations) + " simulations, testing " + str(numIterations*395*6) + " numbers, in " + str(numIterations*395) + " drawings with true randomness: " + str(numTrueWins))
    print("Num wins out of " + str(numIterations) + " simulations, testing " + str(numIterations*395*6) + " numbers, in " + str(numIterations*395) + " drawings with range randomness: " + str(numRangeWins))
    print("Num rand white balls checked: " + str(uniqueWhiteBallsCompared) + "/" + str(totalWhiteBallsGenerated) + " or " + str(uniqueWhiteBallsCompared/totalWhiteBallsGenerated*100) + " percent.")
    print("Num range white balls checked: " + str(uniqueRangeBallsCompared) + "/" + str(totalRangeBallsGenerated) + " or " + str(uniqueRangeBallsCompared/totalRangeBallsGenerated*100) + " percent.")
    return [numTrueWins, numRangeWins]

#This function will run fundamentally differently to the other functions in that it generates the amount of random numbers needed for iterations beforehand rather than as we go through the dataframe
def bulkFastChecker(numIterations):
    timeToRunStart = time.perf_counter()
    numTrueWins = 0
    numRangeWins = 0

    dfAccessTimes = [] 

    #True Random Selection Section
    timeBeforeRandGen = time.perf_counter()
    true_whiteBalls = np.random.randint(70, size=numIterations*395*5) #Because these are ndarrays, access elements in them like an array DONT DELETE IT MAKES NEW OBJECTS WHICH SLOWS PROGRAM
    true_megaBalls =  np.random.randint(25, size=numIterations*395)

    timeAfterRandGen = time.perf_counter()
    timeToRandGen = timeAfterRandGen-timeBeforeRandGen

    print("Total time to generate " + str(numIterations*395*6) + " true random numbers with Numpy: " + str(timeToRandGen))

    #Range Random Selection Section
    timeBeforeRangeGen = time.perf_counter()
    whiteBall1 = np.random.choice([1,2,3,4,7,8,10,11], size=numIterations*395)
    whiteBall2 = np.random.choice([13,16,17,20,22,24,33], size=numIterations*395)
    whiteBall3 = np.random.choice([30,31,34,37,39,41,44,53], size=numIterations*395)
    whiteBall4 = np.random.choice([42,43,48,49,54,56], size=numIterations*395)
    whiteBall5 = np.random.choice([62,64,66,67,68,70], size=numIterations*395)
    range_megaBall = np.random.choice([9,10,11,22], size=numIterations*395)

    timeAfterRangeGen = time.perf_counter()
    timeToRangeGen = timeAfterRangeGen-timeBeforeRangeGen

    # print(str(len(true_megaBalls)) + " should be 0")
    # print(str(len(true_whiteBalls)) + " is number of randomly generated nums")
    # print(str(numSets) + " is the number of randomly generated lotto nums")
    # print(str(timeToGen))
    print("Total time to generate " + str(numIterations*395*6) + " range random numbers with Numpy: " + str(timeToRangeGen))

    #print("Finished Num Generation")
    whiteBallsIndex = 0
    megaBallsIndex = 0
    rangeIndex = 0
    
    for index, row in mainDF.iterrows():
        drawingDayNumbers = [int(row["#1"]), int(row["#2"]), int(row["#3"]), int(row["#4"]), int(row["#5"]), int(row["#6"])]

        #True Random Number Comparison
        for i in range(numIterations):
            sortedNums = [true_whiteBalls[whiteBallsIndex], true_whiteBalls[whiteBallsIndex+1], true_whiteBalls[whiteBallsIndex+2], true_whiteBalls[whiteBallsIndex+3], true_whiteBalls[whiteBallsIndex+4]]
            sortedNums.sort()
            sortedNums.append(true_megaBalls[megaBallsIndex])
            if sortedNums == drawingDayNumbers:
                numTrueWins += 1
                #print("TRUE WINS --- CURRENT TRUE WINS: " + str(numTrueWins))
            #print("Comparison #" + str(i) + "completed")
            whiteBallsIndex += 5
            megaBallsIndex += 1
            
        #Range Random Number Comparison
        for i in range(numIterations):
            sortedNums = [whiteBall1[rangeIndex], whiteBall2[rangeIndex], whiteBall3[rangeIndex], whiteBall4[rangeIndex], whiteBall5[rangeIndex]]
            sortedNums.sort()
            sortedNums.append(range_megaBall[rangeIndex])
            print(sortedNums)
            if sortedNums == drawingDayNumbers:
                numRangeWins+=1
                #print("RANGE WINS --- CURRENT RANGE WINS: " + str(numRangeWins))
            rangeIndex += 1
        whiteBallsIndex = 0
        megaBallsIndex = 0
        rangeIndex = 0
    timeToRunEnd = time.perf_counter()

    print("Num wins out of " + str(numIterations) + " simulations, testing " + str(numIterations*395*6) + " numbers, in " + str(numIterations*395) + " drawings with true randomness: " + str(numTrueWins))
    print("Num wins out of " + str(numIterations) + " simulations, testing " + str(numIterations*395*6) + " numbers, in " + str(numIterations*395) + " drawings with range randomness: " + str(numRangeWins))
    print("Ran in " + str(timeToRunEnd-timeToRunStart) + " seconds")
    return [numTrueWins, numRangeWins]

#The fastest of the functions that generate random lotto numbers procedurally. Time was saved by minimizing dataframe accesses.
def fastCheckerSingleNumberGen():
    numTrueWins = 0
    numRangeWins = 0
    numSumWins = 0
    trueRandNumGenTimes = []
    rangeRandNumGenTimes = []
    sumRandNumGenTimes = []
    dfAccessTimes = []
    #True Random Selection Section
    timeBeforeRandGen = time.perf_counter()
    true_whiteBalls = sorted(sample(range(1,70),5))
    true_megaBall = randrange(1,25)
    true_generatedNumbers = true_whiteBalls + [true_megaBall]
    timeAfterRandGen = time.perf_counter()
    trueRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

    #Range Random Selection Section
    timeBeforeRandGen = time.perf_counter()
    whiteBall1 = choice([1,2,3,4,7,8,10,11])
    whiteBall2 = choice([13,16,17,22,24,33])
    whiteBall3 = choice([31,34,35,39,41,44,53])
    whiteBall4 = choice([42,43,46,48,49,54,56,61])
    whiteBall5 = choice([58,60,62,64,66,67,68,69,70])
    range_megaBall = choice([6,9,10,11,14,22])
    range_generatedNumbers = [whiteBall1,whiteBall2,whiteBall3,whiteBall4,whiteBall5,range_megaBall] 
    timeAfterRandGen = time.perf_counter()
    rangeRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

    #Sum Random Selection Section
    timeBeforeRandGen = time.perf_counter()
    sum_generatedNumbers = []
    summation = 0
    while summation < 104 or summation > 171:
        whiteBalls = sorted(sample(range(1,70),5))
        megaBall = randrange(1,25)
        sum_generatedNumbers = whiteBalls + [megaBall]
        summation = sum(sum_generatedNumbers)
    timeAfterRandGen = time.perf_counter()
    sumRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

    for index, row in mainDF.iterrows():
        timeBeforeDFAccess = time.perf_counter()
        drawingDayNumbers = [int(row["#1"]), int(row["#2"]), int(row["#3"]), int(row["#4"]), int(row["#5"]), int(row["#6"])]
        timeAfterDFAccess = time.perf_counter()
        dfAccessTimes.append(timeAfterDFAccess-timeBeforeDFAccess)
        if true_generatedNumbers == drawingDayNumbers:
            numTrueWins+=1
        if range_generatedNumbers == drawingDayNumbers:
            numRangeWins+=1
        if sum_generatedNumbers == drawingDayNumbers:
            numSumWins+=1

    return [numTrueWins,numRangeWins,numSumWins, sum(trueRandNumGenTimes)/len(trueRandNumGenTimes), sum(rangeRandNumGenTimes)/len(rangeRandNumGenTimes), sum(sumRandNumGenTimes)/len(sumRandNumGenTimes)]

#Changed range random generation to use choice instead of sample
def fastChecker3():
    numTrueWins = 0
    numRangeWins = 0
    numSumWins = 0
    trueRandNumGenTimes = []
    rangeRandNumGenTimes = []
    sumRandNumGenTimes = []
    dfAccessTimes = []
    for index, row in mainDF.iterrows():

        #True Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        true_whiteBalls = sorted(sample(range(1,70),5))
        true_megaBall = randrange(1,25)
        true_generatedNumbers = true_whiteBalls + [true_megaBall]
        timeAfterRandGen = time.perf_counter()
        trueRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        #Range Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        whiteBall1 = choice([1,2,3,4,7,8,10,11])
        whiteBall2 = choice([13,16,17,22,24,33])
        whiteBall3 = choice([31,34,35,39,41,44,53])
        whiteBall4 = choice([42,43,46,48,49,54,56,61])
        whiteBall5 = choice([58,60,62,64,66,67,68,69,70])
        range_megaBall = choice([6,9,10,11,14,22])
        range_generatedNumbers = [whiteBall1,whiteBall2,whiteBall3,whiteBall4,whiteBall5,range_megaBall] 
        timeAfterRandGen = time.perf_counter()
        rangeRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        #Sum Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        sum_generatedNumbers = []
        summation = 0
        while summation < 104 or summation > 171:
            whiteBalls = sorted(sample(range(1,70),5))
            megaBall = randrange(1,25)
            sum_generatedNumbers = whiteBalls + [megaBall]
            summation = sum(sum_generatedNumbers)
        timeAfterRandGen = time.perf_counter()
        sumRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        timeBeforeDFAccess = time.perf_counter()
        drawingDayNumbers = [int(row["#1"]), int(row["#2"]), int(row["#3"]), int(row["#4"]), int(row["#5"]), int(row["#6"])]
        timeAfterDFAccess = time.perf_counter()
        dfAccessTimes.append(timeAfterDFAccess-timeBeforeDFAccess)
        if true_generatedNumbers == drawingDayNumbers:
            numTrueWins+=1
        if range_generatedNumbers == drawingDayNumbers:
            numRangeWins+=1
        if sum_generatedNumbers == drawingDayNumbers:
            numSumWins+=1

    return [numTrueWins,numRangeWins,numSumWins, sum(trueRandNumGenTimes)/len(trueRandNumGenTimes), sum(rangeRandNumGenTimes)/len(rangeRandNumGenTimes), sum(sumRandNumGenTimes)/len(sumRandNumGenTimes)]

#Used iterrows to speed up dataframe accesses
def fastChecker2():
    numTrueWins = 0
    numRangeWins = 0
    numSumWins = 0
    trueRandNumGenTimes = []
    rangeRandNumGenTimes = []
    sumRandNumGenTimes = []
    dfAccessTimes = []
    for index, row in mainDF.iterrows():

        #True Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        true_whiteBalls = sorted(sample(range(1,70),5))
        true_megaBall = randrange(1,25)
        true_generatedNumbers = true_whiteBalls + [true_megaBall]
        timeAfterRandGen = time.perf_counter()
        trueRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        #Range Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        whiteBall1 = sample([1,2,3,4,7,8,10,11],1)
        whiteBall2 = sample([13,16,17,22,24,33],1)
        whiteBall3 = sample([31,34,35,39,41,44,53],1)
        whiteBall4 = sample([42,43,46,48,49,54,56,61],1)
        whiteBall5 = sample([58,60,62,64,66,67,68,69,70],1)
        range_megaBall = sample([6,9,10,11,14,22],1)
        range_generatedNumbers = [whiteBall1,whiteBall2,whiteBall3,whiteBall4,whiteBall5,range_megaBall] 
        timeAfterRandGen = time.perf_counter()
        rangeRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        #Sum Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        sum_generatedNumbers = []
        summation = 0
        while summation < 104 or summation > 171:
            whiteBalls = sorted(sample(range(1,70),5))
            megaBall = randrange(1,25)
            sum_generatedNumbers = whiteBalls + [megaBall]
            summation = sum(sum_generatedNumbers)
        timeAfterRandGen = time.perf_counter()
        sumRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        timeBeforeDFAccess = time.perf_counter()
        drawingDayNumbers = [int(row["#1"]), int(row["#2"]), int(row["#3"]), int(row["#4"]), int(row["#5"]), int(row["#6"])]
        timeAfterDFAccess = time.perf_counter()
        dfAccessTimes.append(timeAfterDFAccess-timeBeforeDFAccess)
        if true_generatedNumbers == drawingDayNumbers:
            numTrueWins+=1
        if range_generatedNumbers == drawingDayNumbers:
            numRangeWins+=1
        if sum_generatedNumbers == drawingDayNumbers:
            numSumWins+=1

    return [numTrueWins,numRangeWins,numSumWins, sum(trueRandNumGenTimes)/len(trueRandNumGenTimes), sum(rangeRandNumGenTimes)/len(rangeRandNumGenTimes), sum(sumRandNumGenTimes)/len(sumRandNumGenTimes)]

#Original lotto number historical comparison function
def fastChecker():
    numTrueWins = 0
    numRangeWins = 0
    numSumWins = 0
    drawingDay = 394
    trueRandNumGenTimes = []
    rangeRandNumGenTimes = []
    sumRandNumGenTimes = []
    dfAccessTimes = []
    while drawingDay >= 0:
        
        #True Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        true_whiteBalls = sorted(sample(range(1,70),5))
        true_megaBall = randrange(1,25)
        true_generatedNumbers = true_whiteBalls + [true_megaBall]
        timeAfterRandGen = time.perf_counter()
        trueRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        #Range Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        whiteBall1 = sample([1,2,3,4,7,8,10,11],1)
        whiteBall2 = sample([13,16,17,22,24,33],1)
        whiteBall3 = sample([31,34,35,39,41,44,53],1)
        whiteBall4 = sample([42,43,46,48,49,54,56,61],1)
        whiteBall5 = sample([58,60,62,64,66,67,68,69,70],1)
        range_megaBall = sample([6,9,10,11,14,22],1)
        range_generatedNumbers = [whiteBall1,whiteBall2,whiteBall3,whiteBall4,whiteBall5,range_megaBall] 
        timeAfterRandGen = time.perf_counter()
        rangeRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        #Sum Random Selection Section
        timeBeforeRandGen = time.perf_counter()
        sum_generatedNumbers = []
        summation = 0
        while summation < 104 or summation > 171:
            whiteBalls = sorted(sample(range(1,70),5))
            megaBall = randrange(1,25)
            sum_generatedNumbers = whiteBalls + [megaBall]
            summation = sum(sum_generatedNumbers)
        timeAfterRandGen = time.perf_counter()
        sumRandNumGenTimes.append(timeAfterRandGen-timeBeforeRandGen)

        timeBeforeDFAccess = time.perf_counter()
        drawingDayNumbers = [int(mainDF.iloc[drawingDay][0]), int(mainDF.iloc[drawingDay][1]), int(mainDF.iloc[drawingDay][2]), int(mainDF.iloc[drawingDay][3]), int(mainDF.iloc[drawingDay][4]), int(mainDF.iloc[drawingDay][5])]
        timeAfterDFAccess = time.perf_counter()
        dfAccessTimes.append(timeAfterDFAccess-timeBeforeDFAccess)
        if true_generatedNumbers == drawingDayNumbers:
            numTrueWins+=1
        if range_generatedNumbers == drawingDayNumbers:
            numRangeWins+=1
        if sum_generatedNumbers == drawingDayNumbers:
            numSumWins+=1
        drawingDay-=1

    return [numTrueWins,numRangeWins,numSumWins, sum(trueRandNumGenTimes)/len(trueRandNumGenTimes), sum(rangeRandNumGenTimes)/len(rangeRandNumGenTimes), sum(sumRandNumGenTimes)/len(sumRandNumGenTimes)]

#The following 3 functions are all components of the above functions and were made first before being integrated into the above functions to save time
def trueRandomGenAndCheck():
    numWins = 0
    drawingDay = 394
    while drawingDay >= 0:
        whiteBalls = sorted(sample(range(1,70),5))
        megaBall = randrange(1,25)
        generatedNumbers = whiteBalls + [megaBall]
        drawingDayNumbers = [int(mainDF.iloc[drawingDay][0]), int(mainDF.iloc[drawingDay][1]), int(mainDF.iloc[drawingDay][2]), int(mainDF.iloc[drawingDay][3]), int(mainDF.iloc[drawingDay][4]), int(mainDF.iloc[drawingDay][5])]
        if generatedNumbers == drawingDayNumbers:
            numWins+=1
        drawingDay-=1
    return numWins    

def rangeRandomGenAndCheck():
    numWins = 0
    drawingDay = 394
    while drawingDay >= 0:
        whiteBall1 = sample([1,2,3,4,7,8,10,11],1)
        whiteBall2 = sample([13,16,17,22,24,33],1)
        whiteBall3 = sample([31,34,35,39,41,44,53],1)
        whiteBall4 = sample([42,43,46,48,49,54,56,61],1)
        whiteBall5 = sample([58,60,62,64,66,67,68,69,70],1)
        megaBall = sample([6,9,10,11,14,22],1)

        generatedNumbers = [whiteBall1,whiteBall2,whiteBall3,whiteBall4,whiteBall5,megaBall]    
        drawingDayNumbers = [int(mainDF.iloc[drawingDay][0]), int(mainDF.iloc[drawingDay][1]), int(mainDF.iloc[drawingDay][2]), int(mainDF.iloc[drawingDay][3]), int(mainDF.iloc[drawingDay][4]), int(mainDF.iloc[drawingDay][5])]
        if generatedNumbers == drawingDayNumbers:
            numWins+=1
        drawingDay-=1
    return numWins

def sumRandomGenAndCheck():
    numWins = 0
    drawingDay = 394
    while drawingDay >= 0:
        generatedNumbers = []
        summation = 0
        while summation < 104 or summation > 171:
            whiteBalls = sorted(sample(range(1,70),5))
            megaBall = randrange(1,25)
            generatedNumbers = whiteBalls + [megaBall]
            summation = sum(generatedNumbers)

        drawingDayNumbers = [int(mainDF.iloc[drawingDay][0]), int(mainDF.iloc[drawingDay][1]), int(mainDF.iloc[drawingDay][2]), int(mainDF.iloc[drawingDay][3]), int(mainDF.iloc[drawingDay][4]), int(mainDF.iloc[drawingDay][5])]
        if generatedNumbers == drawingDayNumbers:
            numWins+=1
        drawingDay-=1
    return numWins

#Driver code for different versions of the program
def simulate(numIterations):
    currentIteration = 0
    cumulativeTrueWins = 0
    cumulativeRangeWins = 0
    cumulativeSumWins = 0
    while currentIteration < numIterations:
        #print(str(currentIteration))
        cumulativeTrueWins += trueRandomGenAndCheck()
        cumulativeRangeWins += rangeRandomGenAndCheck()
        cumulativeSumWins += sumRandomGenAndCheck()
        currentIteration +=1
    # print("-----------------------------------------------")
    # print("Num wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins))
    # print("-----------------------------------------------")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins/numIterations * 100) + " percent.")
    # print("-----------------------------------------------")

def newSimulate(numIterations):
    currentIteration = 0
    cumulativeTrueWins = 0
    cumulativeRangeWins = 0
    cumulativeSumWins = 0
    randNumGenTimes = []
    rangeNumGenTimes = []
    sumNumGenTimes = []
    while currentIteration < numIterations:
        winList = fastChecker()
        cumulativeTrueWins += winList[0]
        cumulativeRangeWins += winList[1]
        cumulativeSumWins += winList[2]
        randNumGenTimes.append(winList[3])
        rangeNumGenTimes.append(winList[4])
        sumNumGenTimes.append(winList[5])
        currentIteration +=1
    # print("Average time to generate a true random number: " + str(sum(randNumGenTimes)/len(randNumGenTimes)))
    # print("Average time to generate a range random number: " + str(sum(rangeNumGenTimes)/len(rangeNumGenTimes)))
    # print("Average time to generate a sum random number: " + str(sum(sumNumGenTimes)/len(sumNumGenTimes)))
    # print("-----------------------------------------------")
    # print("Num wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins))
    # print("-----------------------------------------------")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins/numIterations * 100) + " percent.")
    # print("-----------------------------------------------")

def newSimulate2(numIterations):
    currentIteration = 0
    cumulativeTrueWins = 0
    cumulativeRangeWins = 0
    cumulativeSumWins = 0
    randNumGenTimes = []
    rangeNumGenTimes = []
    sumNumGenTimes = []
    while currentIteration < numIterations:
        winList = fastChecker2()
        cumulativeTrueWins += winList[0]
        cumulativeRangeWins += winList[1]
        cumulativeSumWins += winList[2]
        randNumGenTimes.append(winList[3])
        rangeNumGenTimes.append(winList[4])
        sumNumGenTimes.append(winList[5])
        currentIteration +=1
    # print("Average time to generate a true random number: " + str(sum(randNumGenTimes)/len(randNumGenTimes)))
    # print("Average time to generate a range random number: " + str(sum(rangeNumGenTimes)/len(rangeNumGenTimes)))
    # print("Average time to generate a sum random number: " + str(sum(sumNumGenTimes)/len(sumNumGenTimes)))
    # print("-----------------------------------------------")
    # print("Num wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins))
    # print("-----------------------------------------------")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins/numIterations * 100) + " percent.")
    # print("-----------------------------------------------")

def newSimulate3(numIterations):
    currentIteration = 0
    cumulativeTrueWins = 0
    cumulativeRangeWins = 0
    cumulativeSumWins = 0
    randNumGenTimes = []
    rangeNumGenTimes = []
    sumNumGenTimes = []
    while currentIteration < numIterations:
        winList = fastChecker3()
        cumulativeTrueWins += winList[0]
        cumulativeRangeWins += winList[1]
        cumulativeSumWins += winList[2]
        randNumGenTimes.append(winList[3])
        rangeNumGenTimes.append(winList[4])
        sumNumGenTimes.append(winList[5])
        currentIteration +=1
    # print("Average time to generate a true random number: " + str(sum(randNumGenTimes)/len(randNumGenTimes)))
    # print("Average time to generate a range random number: " + str(sum(rangeNumGenTimes)/len(rangeNumGenTimes)))
    # print("Average time to generate a sum random number: " + str(sum(sumNumGenTimes)/len(sumNumGenTimes)))
    # print("-----------------------------------------------")
    # print("Num wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins))
    # print("-----------------------------------------------")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins/numIterations * 100) + " percent.")
    # print("-----------------------------------------------")

def newSimulate4(numIterations):
    currentIteration = 0
    cumulativeTrueWins = 0
    cumulativeRangeWins = 0
    cumulativeSumWins = 0
    randNumGenTimes = []
    rangeNumGenTimes = []
    sumNumGenTimes = []
    while currentIteration < numIterations:
        winList = fastCheckerSingleNumberGen()
        cumulativeTrueWins += winList[0]
        cumulativeRangeWins += winList[1]
        cumulativeSumWins += winList[2]
        randNumGenTimes.append(winList[3])
        rangeNumGenTimes.append(winList[4])
        sumNumGenTimes.append(winList[5])
        currentIteration +=1

    print("Total time to generate " + str(numIterations) + " true random numbers: " + str(sum(randNumGenTimes)))
    #print("Total time to generate " + str(numIterations) + " range random numbers: " + str(sum(rangeNumGenTimes)))
    #print("Total time to generate " + str(numIterations) + " sum random numbers: " + str(sum(sumNumGenTimes)))
    #print("Total time to generate all random numbers: " + str(sum(sumNumGenTimes) + sum(rangeNumGenTimes) + sum(sumNumGenTimes)))

    # print("Average time to generate a true random number: " + str(sum(randNumGenTimes)/len(randNumGenTimes)))
    # print("Average time to generate a range random number: " + str(sum(rangeNumGenTimes)/len(rangeNumGenTimes)))
    # print("Average time to generate a sum random number: " + str(sum(sumNumGenTimes)/len(sumNumGenTimes)))
    # print("-----------------------------------------------")
    # print("Num wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins))
    # print("Num wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins))
    # print("-----------------------------------------------")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with true randomness: " + str(cumulativeTrueWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with range randomness: " + str(cumulativeRangeWins/numIterations * 100) + " percent.")
    # print("Percent of wins out of " + str(395*numIterations) + " drawings with sum randomness: " + str(cumulativeSumWins/numIterations * 100) + " percent.")
    # print("-----------------------------------------------")

def bulkSimulator():
    i = 1
    totalTrueWins = 0
    totalRangeWins = 0
    print("---------START---SIMULATION---------------")
    while i < 10:
        wins = bulkFastChecker(100000)
        totalTrueWins += wins[0]
        totalRangeWins += wins[1]
        print("--------FINISHED ITERATION " + str(i) + " -------------------------")
        i+=1
    print("TOTAL NUMBER OF TRUE RANDOM WINS: " + str(totalTrueWins))
    print("TOTAL NUMBER OF RANGE RANDOM WINS: " + str(totalRangeWins))
    print("---------END---SIMULATION---------------")


######### CODE TO FIND BEST RANGES ##################
# i = 1
# totalLessWins = 0
# totalBaseWins = 0
# totalMoreWins = 0
# print("---------START---SIMULATION---------------")
# while i < 10:
#     wins = rangesRandomChecker(100000)
#     totalLessWins += wins[0]
#     totalBaseWins += wins[1]
#     totalMoreWins += wins[2]
#     print("--------FINISHED ITERATION " + str(i) + " -------------------------")
#     i+=1
# print("TOTAL NUMBER OF LESS STRICT RANDOM WINS: " + str(totalLessWins))
# print("TOTAL NUMBER OF BASE RANDOM WINS: " + str(totalBaseWins))
# print("TOTAL NUMBER OF MORE STRICT RANDOM WINS: " + str(totalMoreWins))
# print("---------END---SIMULATION---------------")

######### A WHOLE BUNCH OF CODE TO COMPARE RUNTIMES THAT I DIDN"T WANT TO REWRITE SO KEEPING IT HERE ##################
# print("-----------------------------------------------")
# timeBeforeSim = time.perf_counter()
# simulate(1)
# timeAfterSim = time.perf_counter()
# print("Time to simulate with 1 iteration: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate(1)
# timeAfterSim = time.perf_counter()
# print("Time to new simulate with 1 iteration: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate2(1)
# timeAfterSim = time.perf_counter()
# print("Time to new 2 simulate with 1 iteration: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate3(1)
# timeAfterSim = time.perf_counter()
# print("Time to new 3 simulate with 1 iteration: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate4(1)
# timeAfterSim = time.perf_counter()
# print("Time to new 4 simulate with 1 iteration: " + str(timeAfterSim-timeBeforeSim))
# print()

# print("-----------------------------------------------")

# timeBeforeSim = time.perf_counter()
# simulate(10)
# timeAfterSim = time.perf_counter()
# print("Time to simulate with 10 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate(10)
# timeAfterSim = time.perf_counter()
# print("Time to new simulate with 10 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate2(10)
# timeAfterSim = time.perf_counter()
# print("Time to new 2 simulate with 10 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate3(10)
# timeAfterSim = time.perf_counter()
# print("Time to new 3 simulate with 10 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate4(10)
# timeAfterSim = time.perf_counter()
# print("Time to new 4 simulate with 10 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()

# print("-----------------------------------------------")

# timeBeforeSim = time.perf_counter()
# simulate(100)
# timeAfterSim = time.perf_counter()
# print("Time to simulate with 100 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate(100)
# timeAfterSim = time.perf_counter()
# print("Time to new simulate with 100 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate2(100)
# timeAfterSim = time.perf_counter()
# print("Time to new 2 simulate with 100 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate3(100)
# timeAfterSim = time.perf_counter()
# print("Time to new 3 simulate with 100 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()
# timeBeforeSim = time.perf_counter()
# newSimulate4(100)
# timeAfterSim = time.perf_counter()
# print("Time to new 4 simulate with 100 iterations: " + str(timeAfterSim-timeBeforeSim))
# print()

# print("-----------------------------------------------")

