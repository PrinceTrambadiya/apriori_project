from flask import Flask, render_template, request
from csv import reader
import io

app = Flask(__name__)


def getFromFile(fname):
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

    # with open(fname, 'r') as file:
    #     csv_reader = reader(file)
    #     for line in csv_reader:
    #         line = list(filter(None, line))
    #         record = set(line)
    #         for item in record:
    #             itemSet.add(frozenset([item]))
    #         itemSets.append(record)
    return (itemSet, itemSets)


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return list(map(frozenset, C1))


def aprioriGen1(Lk, k):  # creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  # if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j])  # set union
    return retList


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems * 1000

        # support = ssCnt[key]
        # print(support)

        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return (retList, supportData)


def aprioriFromFile(fname, minSup, minConf):
    (C1ItemSet, itemSetList) = getFromFile(fname)

    # print(itemSetList)

    (L1, supportData) = scanD(itemSetList, C1ItemSet, minSup)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = aprioriGen1(L[k - 2], k)
        (Lk, supK) = scanD(itemSetList, Ck, minSup)  # scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return (L, supportData)


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
    (freqItemSet, rules) = aprioriFromFile(output, 20, 0.50)

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
    app.run(debug=False, host="0.0.0.0")
