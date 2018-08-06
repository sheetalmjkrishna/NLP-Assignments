import sys
import re
print ('Hi! This is a performance evaluator \n Please enter your arguments in the following way:\n')
cmdLineArgs = raw_input(
    'eval prediction.txt gold.txt\n')
cmdLineArgs = cmdLineArgs.split()
try:
    with open(cmdLineArgs[1], 'r') as file:
        file1 = (file.read().strip()).split('\n')
        if len(file1)==1:
            file1 = (file1[0].strip()).split('\r')
        predictionFile=[]
        for item in file1:
            item2 = {}
            item2["tag"]=item.split()[0]
            item2["term"]=item.split()[1]
            predictionFile.append(item2)
    file.close()
except BaseException as e:
    print('Unable to open prediction file OR file doesn\'t exist. \n Detailed exception is: \n' + str(e))
    sys.exit()
try:
    with open(cmdLineArgs[2], 'r') as file:
        file2 = (file.read().strip()).split('\n')
        goldFile = []
        for item in file2:
            item2 = {}
            item2["tag"] = item.split()[0]
            item2["term"] = item.split()[1]
            goldFile.append(item2)
except BaseException as e:
    print('Unable to open gold file OR file doesn\'t exist. \n Detailed exception is: \n' + str(e))
    sys.exit()
compressedPrediction=[]
for i,item in enumerate(predictionFile):
    item2={}
    if item["tag"] in ["B-ORG","B-PER","B-LOC","b-org","b-per","b-loc"]:
        item2["tag"]=item["tag"].upper()
        str1=item["term"]
        len1=i+1
        len2=i+1
        j=i+1
        while j<> len(predictionFile) and predictionFile[j]["tag"] == "I-"+item2["tag"].split("-")[1]:
            str1+=(" "+predictionFile[j]["term"])
            len2=j+1
            j+=1
        range="["+str(len1)+"-"+str(len2)+"]"
        item2["term"]=str1+" "+range
        compressedPrediction.append(item2)
compressedGold=[]
for i,item in enumerate(goldFile):
    item2={}
    if item["tag"] in ["B-ORG","B-PER","B-LOC","b-org","b-per","b-loc"]:
        item2["tag"]=item["tag"].upper()
        str1=item["term"]
        len1=i+1
        len2=i+1
        j=i+1
        while j<> len(goldFile) and goldFile[j]["tag"] == "I-"+item2["tag"].split("-")[1]:
            str1+=(" "+goldFile[j]["term"])
            len2=j+1
            j+=1
        range="["+str(len1)+"-"+str(len2)+"]"
        item2["term"]=str1+" "+range
        compressedGold.append(item2)
MyEvalFile = open("eval.txt", "w")
sumNumRecall=0
sumDenRecall=0
sumDenPrecision=0
for tag in ["B-PER","B-LOC","B-ORG"]:
    num=0
    items1=[elem["term"] for elem in compressedPrediction if elem["tag"]==tag]
    items2=[elem["term"] for elem in compressedGold if elem["tag"]==tag]
    MyEvalFile.write("Correct " + tag.split("-")[1] + " = ")
    toWrite=""
    for k in items2:
        if k in items1:
            num+=1
            toWrite+= k+" | "
    if toWrite=="":
        toWrite="NONE"
    else:
        toWrite=toWrite[:-3]
    MyEvalFile.write(toWrite+"\n")
    recall=tag.split("-")[1]+" = "+(str(num)+"/"+str(len(items2))+"\n" if len(items2)<>0 else "n/a \n")
    sumNumRecall+=num
    sumDenRecall+=len(items2)
    sumDenPrecision+=len(items1)
    precision = tag.split("-")[1] + " = " + (str(num) + "/" + str(len(items1))+"\n\n" if len(items1) <> 0 else "n/a \n\n")
    MyEvalFile.write("Recall "+recall)
    MyEvalFile.write("Precision " + precision)
avgRecall=(str(sumNumRecall)+"/"+str(sumDenRecall))   if sumDenRecall <>0 else "n/a"
avgPrec=(str(sumNumRecall)+"/"+str(sumDenPrecision))   if sumDenPrecision <>0 else "n/a"
MyEvalFile.write("Average Recall = " + avgRecall+"\n")
MyEvalFile.write("Average Precision = " + avgPrec+"\n")
MyEvalFile.close()


