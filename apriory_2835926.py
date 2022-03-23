from csv import reader
from optparse import OptionParser
from apriori_python.utils import *


def getFromFile(fname):
    itemSets = []
    itemSet = set()

    with open(fname, 'r') as file:
        csv_reader = reader(file)
        for line in csv_reader:
            line = list(filter(None, line))
            record = set(line)
            for item in record:
                itemSet.add(frozenset([item]))
            itemSets.append(record)
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


def aprioriFromFile(fname, minSup):
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


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='inputFile',
                         help='CSV filename',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minSup',
                         help='Min support (float)',
                         default=0.5,
                         type='float')

    (options, args) = optparser.parse_args()

    print("inputfile " + options.inputFile)
    print("min_sup " + str(options.minSup))

    freqItemSet, rules = aprioriFromFile(options.inputFile, options.minSup)

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
    print(finalList)
    print("End - total items: " + str(len(finalList)))
