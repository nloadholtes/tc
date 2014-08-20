#!/usr/bin/env python
# encoding: utf-8
"""
load_tweets.py

Created by Hilary Mason on 2010-04-25.
Copyright (c) 2010 Hilary Mason. All rights reserved.
"""

import sys, os
import datetime
import subprocess
import pickle
import pymongo
import tweepy # Twitter API class: http://github.com/joshthecoder/tweepy
from lib import mongodb
from lib import klout
from classifiers.classify_tweets import *
import settings # local app settings

class loadTweets(object):
    DB_NAME = 'tweets'
    USER_COLL_NAME = 'users'

    def __init__(self, debug=False):
        self.debug = debug
        self.db = mongodb.connect(self.DB_NAME)
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_KEY, settings.ACCESS_SECRET)
        self.api = tweepy.API(auth)

        last_tweet_id = self.get_last_tweet_id()
        try:
            self.fetchTweets(last_tweet_id)
        except tweepy.error.TweepError: # authorization failure
            print "You need to authorize tc to connect to your twitter account. I'm going to open a browser. Once you authorize, I'll ask for your PIN."
            auth = self.setup_auth()
            self.api = tweepy.API(auth)
            self.fetchTweets(last_tweet_id)

        self.classify_tweets()


    def get_last_tweet_id(self):
        for r in self.db[self.DB_NAME].find(fields={'id': True}).sort('id',direction=pymongo.DESCENDING).limit(1):
            return r['id']

    def fetchTweets(self, since_id=None):
        if since_id:
            tweets = self.api.home_timeline(since_id, count=500)
        else:
            tweets = self.api.home_timeline(count=500)

        ts, authors = self.parse_tweets(tweets)

        self.update_authors(authors)

        # insert into db
        try:
            self.db[self.DB_NAME].insert(ts)
        except pymongo.errors.InvalidOperation: # no tweets?
            pass

        if self.debug:
            print "added %s tweets to the db" % (len(ts))

    def retrieve_search_results(self, searchstr):
        searchresults = self.api.search(q=searchstr)
        results = []
        for result in searchresults:
            item = {
                "created_at": result.created_at,
                "from_user_id": result.from_user_id,
                "id_str": result.id_str,
                "text": result.text,
                "iso_language_code": result.iso_language_code,
            }
            results.append(item)
        return results

    def save_tweet(self, tweet, collection):
        try:
            self.db[collection].insert(tweet)
        except Exception as e:
            print("Error seen while saving tweet:" +str (e))

    def update_tweet(self, tweet, collection):
        try:
            self.db[collection].update({"_id":tweet._id}, tweet, safe=True)
        except Exception as e:
            print("Error seen while updating tweet:" + str(e))

    def get_stored_tweets(self, collection):
        """Return what we've already stored in Mongo"""
        output = self.db[collection].find()
        return output

    def parse_tweets(self, tweets):
        # parse each incoming tweet
        ts = []
        authors = []
        for tweet in tweets:
            t = {
            'author': tweet.author.screen_name,
            'contributors': tweet.contributors,
            'coordinates': tweet.coordinates,
            'created_at': tweet.created_at,
            # 'destroy': tweet.destroy,
            # 'favorite': tweet.favorite,
            'favorited': tweet.favorited,
            'geo': tweet.geo,
            'id': tweet.id,
            'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
            'in_reply_to_status_id': tweet.in_reply_to_status_id,
            'in_reply_to_user_id': tweet.in_reply_to_user_id,
            # 'parse': tweet.parse,
            # 'parse_list': tweet.parse_list,
            #'place': tweet.place,
            # 'retweet': dir(tweet.retweet),
            # 'retweets': dir(tweet.retweets),
            'source': tweet.source,
            # 'source_url': tweet.source_url,
            'text': tweet.text,
            'truncated': tweet.truncated,
            'user': tweet.user.screen_name,
            }
            u = {
            '_id': tweet.author.screen_name, # use as mongo primary key
            'contributors_enabled': tweet.author.contributors_enabled,
            'created_at': tweet.author.created_at,
            'description': tweet.author.description,
            'favourites_count': tweet.author.favourites_count, # beware the british
            'follow_request_sent': tweet.author.follow_request_sent,
            'followers_count': tweet.author.followers_count,
            'following': tweet.author.following,
            'friends_count': tweet.author.friends_count,
            'geo_enabled': tweet.author.geo_enabled,
            'twitter_user_id': tweet.author.id,
            'lang': tweet.author.lang,
            'listed_count': tweet.author.listed_count,
            'location': tweet.author.location,
            'name': tweet.author.name,
            'notifications': tweet.author.notifications,
            'profile_image_url': tweet.author.profile_image_url,
            'protected': tweet.author.protected,
            'statuses_count': tweet.author.statuses_count,
            'time_zone': tweet.author.time_zone,
            'url': tweet.author.url,
            'utc_offset': tweet.author.utc_offset,
            'verified': tweet.author.verified,
            '_updated': datetime.datetime.now(),
            }
            authors.append(u)
            ts.append(t)
        return ts, authors

    def update_authors(self, authors):
        k = klout.KloutAPI(settings.KLOUT_API_KEY)
        update_count = 0

        for user in authors:
            records = [r for r in self.db[self.USER_COLL_NAME].find(spec={'_id': user['_id']})]
            if not records or abs(records[0]['_updated'] - datetime.datetime.now()) >= datetime.timedelta(1): # update once per day
                kwargs = { 'users': user['_id'] }
                try:
                    response = k.call('klout', **kwargs)
                    #                    user['klout_score'] = response['users'][0]['kscore']
                except klout.KloutError: # probably a 404
                    pass
                else:
                    if 'users' in response:
                        user['klout_score'] = response['users'][0]['kscore']
                        self.db[self.USER_COLL_NAME].remove({'_id': user['_id']})
                self.db[self.USER_COLL_NAME].insert(user)
                update_count += 1

        if self.debug:
            print "updated %s users in the db" % (update_count)


    def classify_tweets(self):
        classifiers = []
        for active_classifier in active_classifiers:
            c = globals()[active_classifier]()
            classifiers.append(c)

        for r in self.db[self.DB_NAME].find(spec={'topics': {'$exists': False } },fields={'text': True, 'user': True}): # for all unclassified tweets
            topics = {}
            for c in classifiers:
                (topic, score) = c.classify(r['text'])
                topics[topic] = score

            self.db[self.DB_NAME].update({'_id': r['_id']}, {'$set': {'topics': topics }})


    # util classes
    def setup_auth(self):
        """
        setup_auth: authorize tc with oath
        """
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
        p = subprocess.Popen("open %s" % auth_url, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print "( if the browser fails to open, please go to: %s )" % auth_url
        verifier = raw_input("What's your PIN: ").strip()
        auth.get_access_token(verifier)
        pickle.dump((auth.access_token.key, auth.access_token.secret), open('settings_twitter_creds','w'))
        return auth

    def init_twitter(self, username, password):
        auth = tweepy.BasicAuthHandler(username, password)
        api = tweepy.API(auth)
        return api


if __name__ == '__main__':
    l = loadTweets(debug=True)
