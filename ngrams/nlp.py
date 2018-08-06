import sys
import re
import collections
import math
import random

print ('Hi! This is an ngram parser. Please enter your arguments in the following way:\n')
cmdLineArgs = raw_input(
    'ngrams <training file> -test <test file> \n OR \nngrams <training file> -gen <seeds file> \n');
cmdLineArgs = cmdLineArgs.split();
if len(cmdLineArgs) < 4:
    print ('Insufficient arguments.')
    sys.exit();
if cmdLineArgs[0] != 'ngrams':
    print ('Can\'t recognise ' + cmdLineArgs[0]);
if cmdLineArgs[2] != '-test' and cmdLineArgs[2] != '-gen':
    print ('Can\'t recognise ' + cmdLineArgs[2]);
try:
    with open(cmdLineArgs[1], 'r') as trainingFile:
        data = 'phi ' + re.sub('\s+', ' ', trainingFile.read().replace('\n', ' phi ').lower()).strip();
        trainingFile.close();
except:
    print('Unable to open training file OR file doesn\'t exist.');
    sys.exit();
try:
    if cmdLineArgs[2] == '-test':
        with open(cmdLineArgs[3], 'r') as testFile:
            testData = re.sub('\s+', ' ', testFile.read().replace('\n', '$$').lower()).strip();
            testFile.close();
    else:
        with open(cmdLineArgs[3], 'r') as seedFile:
            seeds = re.sub('\s+', ' ', seedFile.read().replace('\n', ' ').lower()).strip().split();
            seedFile.close();
except:
    print('Unable to open test file OR file doesn\'t exist.');
    sys.exit();

# Initial checks over. Main prog begins.
# Unigram Model
corpusForUnigram = data.replace('phi ', '').split();
listOfUnigramFrequencies = collections.Counter(corpusForUnigram);
listOfUnigramProbabilities = {};
totalNumberOfWords = len(corpusForUnigram);
for item in listOfUnigramFrequencies:
    listOfUnigramProbabilities[item] = float(listOfUnigramFrequencies[item]) / totalNumberOfWords;
# print "-------------------------------------------------------------------------";
# print "\n UNSMOOTHED UNIGRAM LANGUAGE MODEL: \n\n WORD \t FREQUENCY \t PROBABILITY = f/N \n";
# for item in listOfUnigramFrequencies:
# print (' '+item +'\t     '+ str(listOfUnigramFrequencies[item]) + '\t\t   '+ str(listOfUnigramProbabilities[item]));
del corpusForUnigram;
# Bigram Model
corpusForBigram = data.split() if data.rsplit(None, 1)[-1] <> 'phi' else data[:-5].split();
listOfUnigramFrequencies["phi"] = corpusForBigram.count("phi");
listOfBigramFrequencies = {};
listOfBigramProbabilitiesNoSmooth = {};
listOfBigramProbabilitiesSmooth = {};
totalNumberOfWords = len(corpusForBigram);
for index in range(1, totalNumberOfWords):
    if corpusForBigram[index]=='phi':
        continue;
    bigram = corpusForBigram[index] + ' | ' + corpusForBigram[index - 1];
    if bigram in listOfBigramFrequencies:
        listOfBigramFrequencies[bigram] += 1;
    else:
        listOfBigramFrequencies[bigram] = 1;
for item in listOfBigramFrequencies:
    denominator = listOfUnigramFrequencies[item.split()[2]];
    listOfBigramProbabilitiesNoSmooth[item] = float(listOfBigramFrequencies[item]) / denominator;
    listOfBigramProbabilitiesSmooth[item] = float(listOfBigramFrequencies[item] + 1) / (denominator + len(listOfUnigramFrequencies) + 1);
# print "-------------------------------------------------------------------------";
# print "\n UNSMOOTHED BIGRAM LANGUAGE MODEL: \n\n WORDS \t\t FREQUENCY  PROBABILITY = f/N \n";
# for item in listOfBigramFrequencies:
# print (' '+item +'\t     '+ str(listOfBigramFrequencies[item]) + '\t\t'+ str(listOfBigramProbabilitiesNoSmooth[item]));
# print "-------------------------------------------------------------------------";
# print "\n SMOOTHED BIGRAM LANGUAGE MODEL: \n\n WORDS \t\t FREQUENCY  PROBABILITY = f/N \n";
# for item in listOfBigramFrequencies:
# print (' '+item +'\t     '+ str(listOfBigramFrequencies[item]) + '\t\t'+ str(listOfBigramProbabilitiesSmooth[item]));
del corpusForBigram;
def getNewWord(newWord):
    r = re.compile(".*" + newWord+"$");
    listOfBigrams = filter(r.match, listOfBigramFrequencies.keys());
    randProbability = random.random();
    closestBigram = listOfBigrams[0];
    listOfBigramProb = {};
    sumOfFreq = 0;
    for bigram in listOfBigrams:
        listOfBigramProb[bigram] = listOfBigramFrequencies[bigram]
        sumOfFreq += listOfBigramFrequencies[bigram]

    listOfBigramProb.update((x, float(y) / sumOfFreq) for x, y in listOfBigramProb.items())
    temp = 0
    for i,bigram in enumerate(listOfBigrams):
        if i==0:
            temp=listOfBigramProb[bigram];
            continue;
        listOfBigramProb[bigram]+=temp;
        temp=listOfBigramProb[bigram];

    for bigram in listOfBigrams:
        if abs(listOfBigramProb[bigram] - randProbability) < abs(listOfBigramProb[closestBigram] - randProbability):
            closestBigram = bigram;
    return closestBigram.split()[0];


if cmdLineArgs[2] == '-test':
    sentences = testData.split("$$") if testData.rsplit(None, 1)[-1] <> '$$' else testData[:-2].split("$$"); 
    for sentence in sentences:
        print "\n \n S = " + sentence + "\n";
        words = sentence.split();
        uni = 1;
        biNoSmo = 1;
        biSmo = 1;
        for word in words:
            uni = uni * listOfUnigramProbabilities[word];
        words.insert(0, "phi");
        for index in range(1, len(words)):
            bigram = words[index] + ' | ' + words[index - 1];
            biNoSmo = biNoSmo * listOfBigramProbabilitiesNoSmooth[bigram] if bigram in listOfBigramProbabilitiesNoSmooth else 0;
            probIfUnseen = 1.0 / (listOfUnigramFrequencies[bigram.split()[2]] + len(listOfUnigramFrequencies) + 1);
            biSmo = biSmo * listOfBigramProbabilitiesSmooth[bigram] if bigram in listOfBigramProbabilitiesSmooth else probIfUnseen;
            #print str(round(math.log(probIfUnseen, 2), 4))+" "+str(round(math.log(biSmo, 2), 4))
        uni = round(math.log(uni, 2), 4) if uni <> 0 else "undefined";
        biNoSmo = round(math.log(biNoSmo, 2), 4) if biNoSmo <> 0 else "undefined";
        biSmo = round(math.log(biSmo, 2), 4); 
        print "Unsmoothed Unigrams, Logspace(S) : " + str(uni);
        print "Unsmoothed Bigrams, Logspace(S) : " + str(biNoSmo);
        print "Smoothed Bigrams, Logspace(S) : " + str(biSmo);
else:
    for seed in seeds:
        print("\n");
        print " Seed = "+seed + ":\n";
        for i in range(1, 11):
            newWord = seed;
            wordCount = 1;
            sentence = seed;
            while newWord not in ['!', '.', '?'] and wordCount < 10 and newWord <> None:
                newWord = getNewWord(newWord);
                sentence += " " + newWord;
                wordCount += 1;
            print str(i) + ". " + sentence + "\n";
