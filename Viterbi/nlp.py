import sys
import math
from copy import deepcopy

print ('Hi! This is a viterbi parser. Please enter your arguments in the following way:\n')
cmdLineArgs = raw_input(
    'viterbi <probabilities file> <sentences file> \n')
cmdLineArgs = cmdLineArgs.split()
if len(cmdLineArgs) < 3:
    print ('Insufficient arguments.')
    sys.exit()
if cmdLineArgs[0] != 'viterbi':
    print ('Can\'t recognise ' + cmdLineArgs[0])
probabilities = {}
backPtr = []
forPtr = []
try:
    with open(cmdLineArgs[1], 'r') as probFile:
        tempLines = probFile.read().strip().split('\n')
        for line in tempLines:
            words = line.split()
            probabilities[words[0] + ' | ' + words[1]] = float(words[2])
        probFile.close()
        del tempLines
        del words
except:
    print('Unable to open probability file OR file doesn\'t exist.')
    sys.exit()
try:
    with open(cmdLineArgs[2], 'r') as sentFile:
        sentences = sentFile.read().strip().split('\n')
        sentFile.close()
except:
    print('Unable to open sentence file OR file doesn\'t exist.')
    sys.exit()


def getNonZeroProbs(w1, w2, symbol, probs):
    return probs[w1 + ' ' + symbol + ' ' + w2] if w1 + ' ' + symbol + ' ' + w2 in probs else 0.0001


tags = ['noun', 'verb', 'inf', 'prep']


def calcWordEqTagProb(curWord, prevWord, tag, probs):
    if prevWord == 'phi':
        prob = getNonZeroProbs(curWord, tag, '|', probs) * getNonZeroProbs(tag, prevWord, '|', probs)
        backPtr.append(curWord + ' = ' + tag + ' = 0')
        forPtr.append(curWord + ' = ' + tag + ' = ' + str(prob))
    else:
        options1 = []
        for tag1 in tags:
            temp = getNonZeroProbs(tag, tag1, '|', probs) * getNonZeroProbs(prevWord, tag1, '=', probs)
            options1.append(temp)
        options2 = []
        for tag1 in tags:
            matching = [s for s in forPtr if prevWord+' = '+tag1 in s]
            temp =  float(matching[-1].split()[4])* getNonZeroProbs(tag, tag1, '|', probs)
            options2.append(temp)
        prob = getNonZeroProbs(curWord, tag, '|', probs) * max(options1)
        backPtr.append(curWord + ' = ' + tag + ' = ' + tags[options1.index(max(options1))])
        forPtr.append(curWord + ' = ' + tag + ' = ' + str(getNonZeroProbs(curWord, tag, '|', probs)*sum(options2)))
    return prob


def assignMax(tertiaryProbList):
    maxVal = tertiaryProbList[tertiaryProbList.keys()[0]]
    maxKey = tertiaryProbList.keys()[0]
    for item in tertiaryProbList:
        if tertiaryProbList[item] > maxVal:
            maxVal = tertiaryProbList[item]
            maxKey = item
    return maxKey + ' : ' + str(maxVal)


primaryProbList = {}
for sentence in sentences:
    print '\n \nPROCESSING SENTENCE: ' + sentence + '\n \n' + 'FINAL VITERBI NETWORK: \n'
    sentence = 'phi ' + sentence  # adding start of sentence marker
    words = sentence.split()
    secondaryProbList = {}
    probs = deepcopy(probabilities)
    maxProbList = []
    for index in range(1, len(words)):  # start from second word
        tertiaryProbList = {}
        for tag in tags:
            ans = calcWordEqTagProb(words[index], words[index - 1], tag, probs)
            probs[words[index] + ' = ' + tag] = ans
            tertiaryProbList[words[index] + ' = ' + tag] = ans
            print 'P(' + words[index] + ' = ' + tag + ') = ' + str(round(math.log(ans, 2), 4))
        secondaryProbList[words[index]+str(index)] = tertiaryProbList
        maxProbList.append(assignMax(tertiaryProbList))
    secondaryProbList["max"] = maxProbList
    secondaryProbList["seqSums"]=forPtr
    primaryProbList[sentence] = secondaryProbList
    print '\n\nFINAL BACKPTR NETWORK: \n'
    for i, item in enumerate(backPtr):
        if i > 3:
            temp = item.split()
            print 'BackPtr(' + temp[0] + temp[1] + temp[2] + ')' + ' = ' + temp[4]
    # total=0
    # for maxVal in primaryProbList[sentence]["max"]:
    # total+=primaryProbList[sentence]["max"][maxVal]
    lastVal = float(primaryProbList[sentence]["max"][len(primaryProbList[sentence]["max"]) - 1].split()[4])
    print '\n\nBEST TAG SEQUENCE HAS LOG PROBABILITY = ' + str(round(math.log(lastVal, 2), 4))
    for maxVal in reversed(primaryProbList[sentence]["max"]):
        temp = maxVal.replace('=', '->').split()
        print temp[0] + ' ' + temp[1] + ' ' + temp[2]
    print '\n\nFORWARD ALGORITHM RESULTS: \n'
    total = 0
    for i in range(0, len(forPtr)):
        if i % 4 == 0:
            #find all occurrences of this word
            total = float(forPtr[i].split()[4]) + float(forPtr[i + 1].split()[4]) + float(forPtr[i + 2].split()[4]) + float(forPtr[i + 3].split()[4])
        temp = forPtr[i].split()
        print 'P(' + temp[0] + temp[1] + temp[2] + ')' + ' = ' +str(round(float(temp[4])/total, 4)) #temp[4]

    backPtr = []
    forPtr = []

