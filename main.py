from flask import Flask, render_template, request
from csv import reader
import io
import time

app = Flask(__name__)

def dataSorting(iteamSets, sizeOfItemSets):
    retList = []
    lenLk = len(iteamSets)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            tempList1 = list(iteamSets[i])[:sizeOfItemSets - 2]
            tempList2 = list(iteamSets[j])[:sizeOfItemSets - 2]
            tempList1.sort()
            tempList2.sort()
            if tempList1 == tempList2:
                retList.append(iteamSets[i] | iteamSets[j])
    return retList

def scanData(data, Ck, minSupport):
    scanCount = {}
    for id in data:
        for can in Ck:
            if can.issubset(id):
                if not can in scanCount:
                    scanCount[can] = 1
                else:
                    scanCount[can] += 1
    totalItems = float(len(data))
    retList = []
    supportData = {}
    for key in scanCount:
        support = scanCount[key] / totalItems * 1000
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return (retList, supportData)

def getDataFromCSV(fname):
    itemSets = []
    itemSet = set()

    # print(fname.read())
    stream = io.StringIO(fname.stream.read().decode("UTF8"), newline=None)
    csv_reader = reader(stream)
    for line in csv_reader:
        # print(line)
        line = list(filter(None, line))
        record = set(line)
        for item in record:
            itemSet.add(frozenset([item]))
        itemSets.append(record)

    return (itemSet, itemSets)


def apriori(fileName, minSupport):
    (itemSet, itemSetList) = getDataFromCSV(fileName)

    # print(itemSetList)

    (scannedList, supportData) = scanData(itemSetList, itemSet, minSupport)
    tempList = [scannedList]
    tempValue = 2
    while len(tempList[tempValue - 2]) > 0:
        Ck = dataSorting(tempList[tempValue - 2], tempValue)
        (iteamSets, supK) = scanData(itemSetList, Ck, minSupport)
        supportData.update(supK)
        tempList.append(iteamSets)
        tempValue += 1
    return (tempList, supportData)

def removeSubsets(freqItemSet):
    tempCombinedIteamSets = []
    for i in freqItemSet:
        for j in i:
            tempCombinedIteamSets.append(j)
    combinedIteamSets = []
    for i in tempCombinedIteamSets:
        combinedIteamSets.append(i)

    for i in range(len(tempCombinedIteamSets)):
        for j in range(i + 1, len(tempCombinedIteamSets)):
            if tempCombinedIteamSets[i].issubset(tempCombinedIteamSets[j]):
                try:
                    if tempCombinedIteamSets[i] in combinedIteamSets:
                        combinedIteamSets.remove(tempCombinedIteamSets[i])
                except:
                    {}
    finalList = []
    for item in combinedIteamSets:
        finalList.append(list(item))
    print(finalList)
    print(len(finalList))
    return finalList


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/resultCSV", methods=['POST', 'GET'])
def resultCSV():
    output = request.files['csv_files']
    minSupp = request.form['minSupp']
    # print(output)
    # print(minSupp)
    # (freqItemSet, rules) = aprioriFromFile("E://Computer_Science//SEM_1//IA//Course_Project//WebSite//CSV_files//1000-out1.csv",20, 0.50)
    start_time = time.time()
    (freqItemSet, rules) = apriori(output, int(minSupp))
    finalList = removeSubsets(freqItemSet)
    final = [finalList, len(finalList), output, minSupp, (time.time() - start_time)]
    return render_template("index.html", name=final)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
