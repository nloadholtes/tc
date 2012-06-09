#
# manual_analyzer.py
# June 9, 2012
# Nick Loadholtes <nick@ironboundsoftware.com>
#
# Various functions for analyzing tweets manual scored
#
import heapq

def getWordFrequencies(tweets):
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
    output = data[-numtrends:]
    output.reverse()
    return output
