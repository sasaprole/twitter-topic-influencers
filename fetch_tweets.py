import config
import twitter
import logging
from pymongo import MongoClient


FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
logging.basicConfig(filename='test.log', format=FORMAT, level=logging.INFO)

api = twitter.Api(consumer_key=config.consumer_key,
                  consumer_secret=config.consumer_secret,
                  access_token_key=config.access_token_key,
                  access_token_secret=config.access_token_secret)

client = MongoClient()

terms = ["Fashion Tech",
         "Wearables",
         "Cycling",
         "Safety",
         "Road Safety",
         "Traffic Safety",
         "Visibility"]


ct = client.cycle_tweets
ct_search_results = ct.search_results

for term in terms:
    search_result = api.GetSearch(term=term, count=180)
    logging.info("Completed search for '%s'. Number of tweets returned: %s", term, str(len(search_result)))
    for status in search_result:
        status = status.AsDict()
        status['term'] = term
        ct_search_results.find_one_and_update(
                {'tweet_id':status['id']},
                {'$set':status},
                upsert=True)