import logging

class TweetFetcher():
    
    FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='/home/sasa.prole/jobs/test.log', format=FORMAT, level=logging.INFO)
    def __init__(self, list_of_topics, twitter_api, collection):
        self.twitter_api = twitter_api
        self.list_of_topics = list_of_topics
        self.collection = collection
        
    def fetch(self):            
        self.statuses = []
        for topic in self.list_of_topics:
            search_result = self.twitter_api.GetSearch(term=topic, count=180)
            logging.info("Completed search for '%s'. Number of tweets returned: %s", topic, str(len(search_result)))

            for status in search_result:
                status = status.AsDict()
                status['term'] = topic
                if 'terms' not in status.keys():
                    status['terms'] = [topic]
                if status['term'] not in status['terms']:
                    status['terms'].append(status['term'])
                self.statuses.append(status)
        return self.statuses
    
    def save(self):
        for status in self.statuses:
            status_temp = self.collection.find_one({'tweet_id':status['id']})
            if status_temp is not None:
                if 'terms' in status_temp.keys():
                    status['terms'] = status['terms'] + status_temp['terms']
            status['terms'] = list(set(status['terms']))
            self.collection.find_one_and_update(
                {'tweet_id':status['id']},
                {'$set':status},
                upsert=True)