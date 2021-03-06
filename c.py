#
# c.py
#
# Nick Loadholtes <nick@ironboundsoftware.com>
# An Experiment in clustering tweets
#

def clusterOnTweets(tweets):
    """Take the tweets, create clusters of similar tweets"""
    words = []
    clusters = []
    for tweet in tweets:
        text = tweet.text
        wordlist = text.split(' ')
        words.append(wordlist)

    print(str(words))

    #Loops through the words, bringing together similar scores
    return clusters


if __name__ == "__main__":
    print("Clustering experiment")
    #Get tweets
    tweets = []
    clusterOnTweets(tweets)

