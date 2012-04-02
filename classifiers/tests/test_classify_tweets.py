#
# Tests for the classifiers
#
# Nick Loadholtes <nick@ironboundsoftware.com>
# April 1, 2012
#

import unittest

from classifiers.classify_tweets import Emotion

POSITIVE_TWEET = ['I really like the new format']
NEGATIVE_TWEET = ['I really hate the new format']
NEUTRAL_TWEET = ['This is just some text']

class TestEmotion(unittest.TestCase):
    def setUp(self):
        self.c = Emotion()

    def testNegativeEmotion(self):
        self.assertTrue(self.c.classify(NEGATIVE_TWEET[0]) < 0.0)

    def testPositiveEmotion(self):
        self.assertTrue(self.c.classify(POSITIVE_TWEET[0]) > 0.0)

    def testNeutralEmotion(self):
        self.assertTrue(self.c.classify(NEUTRAL_TWEET[0]) == 0.0)
