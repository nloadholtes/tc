#
# manual_analyzer.py
# June 9, 2012
# Nick Loadholtes <nick@ironboundsoftware.com>
#
# Various functions for analyzing tweets manual scored
#
import heapq
import json

def getWordFrequencies(tweets, numwords=25):
    wordmap = {}
    for tweet in tweets:
        for word in tweet:
            score = wordmap.get(word, 0)
            score += 1
            wordmap[word] = score

    #Get the words out of the map in order of score
    items = []
    for key in wordmap:
        heapq.heappush(items, (wordmap[key], key))
    data = [heapq.heappop(items) for x in range(len(items))]
    output = data[-numwords:]
    output.reverse()
    return output

def loadFile(filename):
    f = open(filename,'r')
    output = json.loads(f.read())
    f.close()
    return output
