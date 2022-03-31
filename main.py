from flask import Flask, render_template, request
from csv import reader
import io
import os

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


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/result", methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    name = output["name"]
    return render_template("index.html", name=name)


@app.route("/resultCSV", methods=['POST', 'GET'])
def resultCSV():
    output = request.files['csv_files']
    print(output)
    # (freqItemSet, rules) = aprioriFromFile("E://Computer_Science//SEM_1//IA//Course_Project//WebSite//CSV_files//1000-out1.csv",20, 0.50)
    (freqItemSet, rules) = apriori(output, 20)

    for count in freqItemSet:

        for item1 in freqItemSet[0]:
            for item2 in freqItemSet[1]:
                for item3 in freqItemSet[2]:
                    for item4 in freqItemSet[3]:
                        if item1.issubset(item2) \
                                or item1.issubset(item3) \
                                or item1.issubset(item4):
                            try:
                                freqItemSet[0].remove(item1)
                            except:
                                {}
                        if item2.issubset(item3) \
                                or item2.issubset(item4):
                            try:
                                freqItemSet[1].remove(item2)
                            except:
                                {}
                        if item3.issubset(item4):
                            try:
                                freqItemSet[2].remove(item3)
                            except:
                                {}

    finalList = []
    for item in freqItemSet:
        item.reverse()
        for subItem in item:
            finalList.append(list(subItem))
    return render_template("index.html", name=finalList)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
