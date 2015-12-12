import sys
import os.path
import csv
import math
import types
from collections import defaultdict, Iterable
import itertools
import getdata
import json

class Apriori:
    def __init__(self, restaurant_id, minSup, minConf):
        self.transList = defaultdict(list)
        self.freqList = defaultdict(int)
        self.itemset = set()
        self.name = defaultdict(str)
        self.highSupportList = list()
        self.numItems = 0
        self.prepData(restaurant_id)             # initialize the above collections

        self.F = defaultdict(list)

        self.minSup = minSup
        self.minConf = minConf

    def genAssociations(self):
        candidate = {}
        count = {}

        self.F[1] = self.firstPass(self.freqList, 1)
        k=2
        while len(self.F[k-1]) != 0:
            candidate[k] = self.candidateGen(self.F[k-1], k)
            for t in self.transList.iteritems():
                for c in candidate[k]:
                    if set(c).issubset(t[1]):
                        self.freqList[c] += 1

            self.F[k] = self.prune(candidate[k], k)
            k += 1

        return self.F

    def prune(self, items, k):
        f = []
        for item in items:
            count = self.freqList[item]
            support = self.support(count)
            if support >= .95 * self.numItems:
                self.highSupportList.append(item)
            elif support >= self.minSup:
                f.append(item)

        return f

    def candidateGen(self, items, k):
        candidate = []

        if k == 2:
            candidate = [tuple(sorted([x, y])) for x in items for y in items if len((x, y)) == k and x != y]
        else:
            candidate = [tuple(set(x).union(y)) for x in items for y in items if len(set(x).union(y)) == k and x != y]

        for c in candidate:
            subsets = self.genSubsets(c)
            if any([ x not in items for x in subsets ]):
                candidate.remove(c)

        return set(candidate)

    def genSubsets(self, item):
        subsets = []
        for i in range(1,len(item)):
            subsets.extend(itertools.combinations(item, i))
        return subsets

    def genRules(self, F):
        H = []

        for k, itemset in F.iteritems():
            if k >= 2:
                for item in itemset:
                    subsets = self.genSubsets(item)
                    for subset in subsets:
                        if len(subset) == 1:
                            subCount = self.freqList[subset[0]]
                        else:
                            subCount = self.freqList[subset]
                        itemCount = self.freqList[item]
                        if subCount != 0:
                            confidence = self.confidence(subCount, itemCount)
                            if confidence >= self.minConf:
                                support = self.support(self.freqList[item])
                                rhs = self.difference(item, subset)
                                if len(rhs) == 1:
                                    H.append((subset, rhs, support, confidence))

        return H

    def difference(self, item, subset):
        return tuple(x for x in item if x not in subset)

    def confidence(self, subCount, itemCount):
        return float(itemCount)/subCount

    def support(self, count):
        return count

    def firstPass(self, items, k):
        f = []
        for item, count in items.iteritems():
            support = self.support(count)
            if support == self.numItems:
                self.highSupportList.append(item)
            elif support >= self.minSup:
                f.append(item)

        return f

    """
    Prepare the transaction data into a dictionary
    key: Receipt.id
    val: set(Goods.Id)

    Also generates the frequent itemlist for itemsets of size 1
    key: Goods.Id
    val: frequency of Goods.Id in self.transList
    """
    def prepData(self,restaurant_id):
        data = getdata.get_order(restaurant_id)
        orders = data["hits"]["hits"]
        for order in orders:
            for foods in order["_source"]["detail"]["group"]:
                self.numItems += 1
                key = order["_source"]["order_id"]
                for i, item in enumerate(foods):
                    food_id = item["id"]
                    quantity = item["quantity"]
    #                print key,food_id,quantity
                    self.name[food_id] = item["name"]
                    self.transList[key].append(food_id)
                    self.itemset.add(food_id)
                    self.freqList[food_id] += quantity

    def readable(self,item):
        itemStr = ''
        for k, i in enumerate(item):
           itemStr += self.name[i] +","
        return itemStr

    def saveResultToJson(self,filename):
        res=[]
        frequentItemsets = self.genAssociations()
        rules = self.genRules(frequentItemsets)
        rule_by_item = dict()
        for i,rule in enumerate(rules):
            if self.readable(rule[0]) in rule_by_item:
                rule_by_item[self.readable(rule[0])].append(rule)
            else:
                rule_by_item[self.readable(rule[0])] = [rule]

        for k in rule_by_item:
            rules_aggregated = rule_by_item[k]
            single_rule = dict()
            single_rule_prefix_food = []
            for food in rules_aggregated[0][0]:
                single_rule_prefix_food.append({"id":food,"name":self.name[food]})
            single_rule["prefix_foods"] = single_rule_prefix_food
            single_rule["rules"] = []
            for rule in rules_aggregated:
                rule_dict=dict()
                rule_dict["sup"] = rule[2]
                rule_dict["conf"] = rule[3]
                food_in_rule = []
                for food in rule[1]:
                    food_in_rule.append({"id":food,"name":self.name[food]})
                rule_dict["foods"] = food_in_rule
                single_rule["rules"].append(rule_dict)
            res.append(single_rule)

        with open(filename,"w") as f:
            f.write(json.dumps(res))


def mineAssosiationRule(restaurant_id,minSup=20,minConf=0.01):
    a = Apriori(restaurant_id, minSup, minConf)
    a.saveResultToJson("data/"+str(restaurant_id)+".json")

def getRules(restaurant_id):
    path = "data/"+str(restaurant_id)+".json"
    if not os.path.isfile(path) :
        mineAssosiationRule(restaurant_id)
    with open(path) as f:
        return json.loads(f.read())


def main():
    print(getdata.get_order_by_foods_and_restaurant(279592,s))
    mineAssosiationRule(279592)
    print(getRules(279592))

if __name__ == '__main__':
    main()
