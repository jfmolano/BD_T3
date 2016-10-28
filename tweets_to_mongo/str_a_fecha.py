from pymongo import MongoClient #pip install pymongo
from datetime import datetime

MONGODB_SERVER = "0.0.0.0"
MONGODB_PORT = 27017
MONGODB_DB = "taller3"
TWEETS_COLLECTION = "tweets"
TWEETS_COLLECTION_F = "tweets_fecha"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
tweets_collection = db[TWEETS_COLLECTION]
tweets_collection_fecha = db[TWEETS_COLLECTION_F]

#tweets_l = tweets_collection.find({"id":788010609765978112})
tweets_l = tweets_collection.find({})
i = 0
for tweet in tweets_l:
	fecha = tweet["created_at"]
	date_object = datetime.strptime(fecha, '%a %b %d %H:%M:%S +0000 %Y')
	tweet["fecha"] = date_object
	tweets_collection_fecha.insert(tweet)
	print str(i/(361818.0)*100.0)+" %"
	i = i+1