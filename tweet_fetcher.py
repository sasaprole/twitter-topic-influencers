import logging

class TweetFetcher():
    
    FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='test.log', format=FORMAT, level=logging.INFO)
    def __init__(self, list_of_topics, twitter_api, collection):
        self.twitter_api = twitter_api
        self.list_of_topics = list_of_topics
        self.collection = collection
        
    def fetch(self):
        for topic in self.list_of_topics:
            search_result = self.twitter_api.GetSearch(term=topic, count=180)
            logging.info("Completed search for '%s'. Number of tweets returned: %s", topic, str(len(search_result)))
            self.statuses = []
            for status in search_result:
                status = status.AsDict()
                status['term'] = topic
                self.statuses.append(status)
        return self.statuses
    
    def save(self):
        for status in self.statuses:
            self.collection.find_one_and_update(
                {'tweet_id':status['id']},
                {'$set':status},
                upsert=True)