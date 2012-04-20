#
# manual_classifier.py
# April 20, 2012
# Nick Loadholtes <nick@ironboundsoftware.com>
#
# Manual analysis of tweets
#

import sys
import datetime
import json

if __name__ == '__main__':
    #Load a file
    if len(sys.argv) < 2:
        print("A search query is needed")
        exit(-1)

    f = open(sys.argv[1])
    data = json.loads(f.read())
    f.close()

    #Examine each entry
    results ={'pos':[], 'neg':[],'neutral':[]}
    reallyquit = False
    for text in data:
        print(text)
        tryagain = True
        while tryagain:
            k = raw_input("p,n,o,or q:")
            tryagain = False
            #record + or - or pass
            if k == 'p':
                results['pos'].append(text)
            elif k == 'n':
                results['neg'].append(text)
            elif k == 'o':
                results['neutral'].append(text)
            elif k == 'q':
                reallyquit = True
                break
            else:
                tryagain = True
        if reallyquit:
            break
        #look neg, see most common words

        #look at pos, see most common words

    #write out pos andneg words.
    fout = open('results.json', 'w')
    fout.write(json.dumps(results))
    fout.close()
