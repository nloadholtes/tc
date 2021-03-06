#
# c_test.py
#
# Nick Loadholtes <nick@ironboundsoftware.com>
# Testing an Experiment in clustering tweets
#

import unittest
import c

def genTweet(intext):
    class S():
        text = intext
    return S()

class ClusterTesting(unittest.TestCase):
    def setUp(self):
        self.tweets =[genTweet('first tweet'), genTweet('second tweet'),
                      genTweet('third tweet')]

    def testClusteronTweets(self):
        clusters = c.clusterOnTweets(self.tweets)
        self.assertTrue(clusters is not None)

