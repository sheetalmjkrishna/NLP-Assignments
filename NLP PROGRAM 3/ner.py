import sys
import re

print ('Hi! This is a machine learning classifer for Named Entity Recognition (NER). \n Please enter your arguments in the following way:\n')
cmdLineArgs = raw_input(
    'ner train.txt test.txt locs.txt WORD ABBR LOCATION POSCON POS WORDCON CAP\n')
cmdLineArgs = cmdLineArgs.split()
'''if len(cmdLineArgs) < 3:
    print ('Insufficient arguments.')
    sys.exit()
if cmdLineArgs[0] != 'viterbi':
    print ('Can\'t recognise ' + cmdLineArgs[0])'''
try:
    with open(cmdLineArgs[1], 'r') as file:
        tempLines = (file.read().strip()).split('\n')
        trainingSet = []
        outerItem=[]
        for i,line in enumerate(tempLines):
            if len(line) <> 0:
                item={}
                words = line.split()
                item["label"]=words[0]
                item["pos"] = words[1]
                item["word"] = words[2]
                outerItem.append(item)
                if i==len(tempLines)-1:
                    trainingSet.append(outerItem)
            else:
                if len(outerItem)!=0:
                    trainingSet.append(outerItem)
                    outerItem=[]
    file.close()
    locations = []
    with open(cmdLineArgs[3], 'r') as file:
        tempLines = file.read().strip().split('\n')
        for loc in tempLines:
            if len(loc) <> 0:
                locations.append(loc)
        file.close()
    del file
    del words
    ftype = cmdLineArgs[4:]
    ftype=map(lambda x: x.lower(), ftype)
    if(ftype[0]!="word" or len(ftype)>7):
        print "First ftype isn't 'word' or you've entered more that 7 ftypes."
        sys.exit()
except BaseException as e:
    if str(e)!="":
        print('Unable to open training file OR file doesn\'t exist. \n Detailed exception is: \n'+str(e))
        sys.exit()
MyTrainOutputFile = open("train.txt.readable", "w")
MyTrainOutputFile2 = open("train.txt.vector", "w")
MyTestOutputFile = open("test.txt.readable", "w")
MyTestOutputFile2 = open("test.txt.vector", "w")
#wordVocab=[]
#posVocab=[]
wordConVocab=[]
posConVocab=[]
idchart=[]

bioTags={}
bioTags["O"]=0
bioTags["B-PER"]=1
bioTags["I-PER"]=2
bioTags["B-LOC"]=3
bioTags["I-LOC"]=4
bioTags["B-ORG"]=5
bioTags["I-ORG"]=6

#Building feature vectors
trainingFeatureVectorSet=[]
for item1 in trainingSet:
    outerItem = []
    for i,item2 in enumerate(item1):
        '''
        if item2["word"] not in wordVocab:
            wordVocab.append(item2["word"])
        if item2["pos"] not in posVocab:
            posVocab.append(item2["pos"])
        '''
        item3 = {}
        item3["word"]=item2["word"]
        if("word-"+item3["word"] not in idchart):
            idchart.append("word-"+item3["word"])
        prevWord="PHI" if i==0 else item1[i-1]["word"]
        prevPos="PHIPOS" if i==0 else item1[i-1]["pos"]
        nextWord="OMEGA" if (i==len(item1)-1) else item1[i+1]["word"]
        nextPos="OMEGAPOS" if (i==len(item1)-1) else item1[i+1]["pos"]
        #if item3["word"]=="PM-GreenhouseProgram":
        #    print ""
        item3["wordcon"] = "n/a" if ("wordcon" not in ftype) else prevWord +" "+ nextWord
        if("prev-word-"+prevWord not in idchart and "wordcon" in ftype):
            idchart.append("prev-word-"+prevWord)
        if("next-word-"+nextWord not in idchart and "wordcon" in ftype):
            idchart.append("next-word-"+nextWord)
        item3["pos"] = "n/a" if ("wordcon" not in ftype) else item2["pos"]
        if("pos-"+item3["pos"] not in idchart and "pos" in ftype):
            idchart.append("pos-"+item3["pos"])
        item3["poscon"] = "n/a" if ("poscon" not in ftype) else prevPos +" "+nextPos
        if ("prev-pos-" + prevPos not in idchart and "poscon" in ftype):
            idchart.append("prev-pos-" + prevPos)
        if ("next-pos-" + nextPos not in idchart and "poscon" in ftype):
            idchart.append("next-pos-" + nextPos)
        pattern="^[a-zA-Z.]{1,4}$"
        if ("abbr" not in ftype):
            item3["abbr"] = "n/a"
        else:
            if re.match(pattern, item2["word"]) and item2["word"].endswith('.'):
                item3["abbr"] = "yes"
            else:
                item3["abbr"] = "no"
        if ("abbreviated" not in idchart and "abbr" in ftype):
            idchart.append("abbreviated")
        item3["cap"] = "n/a" if ("cap" not in ftype) else ("yes" if (re.match("[A-Z]+",item2["word"])) else "no")
        if ("capitalized" not in idchart and "cap" in ftype):
            idchart.append("capitalized")
        item3["location"] = "n/a" if ("location" not in ftype) else ("yes" if (item2["word"]in locations) else "no")
        if ("location" not in idchart and "location" in ftype):
            idchart.append("location")

        outerItem.append(item3)
        indexArray=[]
        MyTrainOutputFile2.write(str(bioTags[item2["label"]])+" ")#label
        MyTrainOutputFile.write("WORD: "+item3["word"]+"\n" )
        indexArray.append(idchart.index("word-"+item3["word"])+1)
        #MyTrainOutputFile2.write(str(idchart.index("word-"+item3["word"])+1) + ":1 ")  # word
        MyTrainOutputFile.write("WORDCON: " + item3["wordcon"]+"\n")
        if "wordcon" in ftype:
            indexArray.append(idchart.index("prev-word-"+prevWord)+1)
            indexArray.append(idchart.index("next-word-" + nextWord) + 1)
            #MyTrainOutputFile2.write(str(idchart.index("prev-word-"+prevWord)+1) + ":1 ")  # prev-word
            #MyTrainOutputFile2.write(str(idchart.index("next-word-" + nextWord)+1) + ":1 ")  # next-word
        MyTrainOutputFile.write("POS: " + item3["pos"]+"\n")
        if "pos" in ftype:
            indexArray.append(idchart.index("pos-" + item3["pos"]) + 1)
            #MyTrainOutputFile2.write(str(idchart.index("pos-" + item3["pos"]) + 1) + ":1 ")  # pos
        MyTrainOutputFile.write("POSCON: " + item3["poscon"]+"\n")
        if "poscon" in ftype:
            indexArray.append(idchart.index("prev-pos-" + prevPos) + 1)
            indexArray.append(idchart.index("next-pos-" + nextPos) + 1)
            #MyTrainOutputFile2.write(str(idchart.index("prev-pos-" + prevPos) + 1) + ":1 ")  # prev-pos
            #MyTrainOutputFile2.write(str(idchart.index("next-pos-" + nextPos) + 1) + ":1 ")  # next-pos
        MyTrainOutputFile.write("ABBR: " + item3["abbr"]+"\n")
        if "abbr" in ftype and item3["abbr"]=="yes":
            indexArray.append(idchart.index("abbreviated") + 1)
            #MyTrainOutputFile2.write(str(idchart.index("abbreviated") + 1) + ":1 ")  # abbr
        MyTrainOutputFile.write("CAP: " + item3["cap"]+"\n")
        if "cap" in ftype and item3["cap"] == "yes":
            indexArray.append(idchart.index("capitalized") + 1)
            #MyTrainOutputFile2.write(str(idchart.index("capitalized") + 1) + ":1 ")  # cap
        MyTrainOutputFile.write("LOCATION: " + item3["location"]+"\n \n")
        if "location" in ftype and item3["location"] == "yes":
            indexArray.append(idchart.index("location") + 1)
            #MyTrainOutputFile2.write(str(idchart.index("location") + 1) + ":1 ")  # loc
        indexArray.sort()
        for j in indexArray:
            MyTrainOutputFile2.write(str(j)+":1 ")
        indexArray=[]
        MyTrainOutputFile2.write("\n")

    trainingFeatureVectorSet.append(outerItem)
    #MyTrainOutputFile.write("\n \n \n")
#print idchart
MyTrainOutputFile.close()
MyTrainOutputFile2.close()
idchart.append("word-UNK")
idchart.append("prev-word-UNK")
idchart.append("next-word-UNK")
idchart.append("pos-UNKPOS")
idchart.append("prev-pos-UNKPOS")
idchart.append("next-pos-UNKPOS")


#make vector chart






try:
    with open(cmdLineArgs[2], 'r') as file:
        tempLines = (file.read().strip()).split('\n')
        testingSet = []
        outerItem=[]
        for x,line in enumerate(tempLines):
            if len(line) <> 0:
                item={}
                words = line.split()
                item["label"]=words[0]
                item["pos"] = words[1]
                item["word"] = words[2]
                outerItem.append(item)
                if x==len(tempLines)-1:
                    testingSet.append(outerItem)
            else:
                if len(outerItem)!=0:
                    testingSet.append(outerItem)
                    outerItem=[]
        file.close()
except:
    print('Unable to open training file OR file doesn\'t exist. \n Detailed exception is: \n' + str(e))
    sys.exit()

testingFeatureVectorSet=[]
for item1 in testingSet:
    outerItem = []
    for i,item2 in enumerate(item1):
        item3 = {}
        item3["word"]="UNK" if "word-"+item2["word"] not in idchart else item2["word"]
        prevWord="PHI" if i==0 else ("UNK" if "word-"+item1[i-1]["word"] not in idchart else item1[i-1]["word"])
        prevPos="PHIPOS" if i==0 else ("UNKPOS" if "pos-"+item1[i-1]["pos"] not in idchart else item1[i-1]["pos"])
       # if i<>len(item1)-1 and item1[i+1]["word"]=="Bruce":
            #print ""
        nextWord="OMEGA" if (i==len(item1)-1) else ("UNK" if "word-"+item1[i+1]["word"] not in idchart else item1[i+1]["word"])
        nextPos="OMEGAPOS" if (i==len(item1)-1) else ("UNKPOS" if "pos-"+item1[i+1]["pos"] not in idchart else item1[i+1]["pos"])
        item3["wordcon"] = "n/a" if ("wordcon" not in ftype) else prevWord +" "+ nextWord
        item3["pos"] = "n/a" if ("wordcon" not in ftype) else ("UNKPOS" if "pos-"+item2["pos"] not in idchart else item2["pos"])
        item3["poscon"] = "n/a" if ("poscon" not in ftype) else prevPos +" "+nextPos
        pattern="^[a-zA-Z.]{1,4}$"
        if ("abbr" not in ftype):
            item3["abbr"] = "n/a"
        else:
            if re.match(pattern, item2["word"]) and item2["word"].endswith('.'):
                item3["abbr"] = "yes"
            else:
                item3["abbr"] = "no"

        item3["cap"] = "n/a" if ("cap" not in ftype) else ("yes" if (re.match("[A-Z]+", item2["word"])) else "no")
        item3["location"] = "n/a" if ("location" not in ftype) else ("yes" if (item2["word"]in locations) else "no")
        outerItem.append(item3)
        indexArray = []
        prevWord = "PHI" if i == 0 else ("UNK" if "prev-word-" + item1[i - 1]["word"] not in idchart else item1[i - 1]["word"])
        nextWord = "OMEGA" if (i == len(item1) - 1) else ("UNK" if "next-word-" + item1[i + 1]["word"] not in idchart else item1[i + 1]["word"])
        prevPos = "PHIPOS" if i == 0 else ("UNKPOS" if "prev-pos-" + item1[i - 1]["pos"] not in idchart else item1[i - 1]["pos"])
        nextPos = "OMEGAPOS" if (i == len(item1) - 1) else ("UNKPOS" if "next-pos-" + item1[i + 1]["pos"] not in idchart else item1[i + 1]["pos"])
        MyTestOutputFile2.write(str(bioTags[item2["label"]]) + " ")  # label
        indexArray.append(idchart.index("word-" + item3["word"]) + 1)
        MyTestOutputFile.write("WORD: "+item3["word"]+"\n" )
        MyTestOutputFile.write("WORDCON: " + item3["wordcon"]+"\n")
        if "wordcon" in ftype:
            indexArray.append(idchart.index("prev-word-"+prevWord)+1)
            indexArray.append(idchart.index("next-word-" + nextWord) + 1)
        MyTestOutputFile.write("POS: " + item3["pos"]+"\n")
        if "pos" in ftype:
            indexArray.append(idchart.index("pos-" + item3["pos"]) + 1)
        MyTestOutputFile.write("POSCON: " + item3["poscon"]+"\n")
        if "poscon" in ftype:
            indexArray.append(idchart.index("prev-pos-" + prevPos) + 1)
            indexArray.append(idchart.index("next-pos-" + nextPos) + 1)
        MyTestOutputFile.write("ABBR: " + item3["abbr"]+"\n")
        if "abbr" in ftype and item3["abbr"]=="yes":
            indexArray.append(idchart.index("abbreviated") + 1)
        MyTestOutputFile.write("CAP: " + item3["cap"]+"\n")
        if "cap" in ftype and item3["cap"] == "yes":
            indexArray.append(idchart.index("capitalized") + 1)
        MyTestOutputFile.write("LOCATION: " + item3["location"]+"\n \n")
        if "location" in ftype and item3["location"] == "yes":
            indexArray.append(idchart.index("location") + 1)
        indexArray.sort()
        for k in indexArray:
            MyTestOutputFile2.write(str(k) + ":1 ")
        indexArray = []
        MyTestOutputFile2.write("\n")


    testingFeatureVectorSet.append(outerItem)
    #MyTestOutputFile.write("\n \n \n")
MyTestOutputFile.close()