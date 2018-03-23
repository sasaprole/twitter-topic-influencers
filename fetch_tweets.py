import config
import twitter
from tweet_fetcher import TweetFetcher
from pymongo import MongoClient

api = twitter.Api(consumer_key=config.consumer_key,
                  consumer_secret=config.consumer_secret,
                  access_token_key=config.access_token_key,
                  access_token_secret=config.access_token_secret)

terms = ["Fashion Tech",
         "Wearables",
         "Cycling",
         "Safety",
         "Road Safety",
         "Traffic Safety",
        "Visibility",
		 "#Kickstarter",
		 "#kickstarter",
		 "#Crowdfunding",
		 "#crowdfunding",
		 "#kickstart",
		 "crowdfund",
		 "Kickstarter",
		 "kickstarter",
		 "Crowdfunding",
		 "crowdfunding",
		 "kickstart",
		 "crowdfund"]


client = MongoClient("mongodb://sasaprole:123ChangeMe!!!@localhost")
ct = client.cycle_tweets
ct_search_results = ct.search_results

tf = TweetFetcher(terms, api, ct_search_results)

tf.fetch()
tf.save()