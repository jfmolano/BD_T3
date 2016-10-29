from pymongo import MongoClient #pip install pymongo
#from datetime import date, datetime, time, timedelta
from datetime import datetime, timedelta

MONGODB_SERVER = "0.0.0.0"
MONGODB_PORT = 27017
MONGODB_DB = "taller3"
TWEETS_COLLECTION = "tweets"
ROBOTS_COLLECTION = "consulta_robots"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
tweets_collection = db[TWEETS_COLLECTION]
robots_collection = db[ROBOTS_COLLECTION]

def dar_imagen(user):
	condicion = {"user.screen_name":str(user)}
	imagen = tweets_collection.find(condicion)
	usu = imagen.next()
	return usu["user"]["profile_image_url_https"]

usuarios = tweets_collection.aggregate([
                     { "$group": { 
                         "_id": "$user.screen_name", 
                         "total": { "$sum": 1 }
                         } },
                     { "$match": { "total": {"$gt":3000} } }
                   ])

objeto = {}
for usuario in usuarios:
	try:
		user = usuario["_id"]
		print user
		robots = tweets_collection.aggregate([
	                     { "$match": {"text" : {"$regex" : ".*@"+user+".*"},"user.followers_count":{ "$lt": 1000 }}},
	                     { "$group": { 
	                         "_id": {"user":"$user.screen_name","hora":{ "$hour": "$fecha" },"mes":{ "$month": "$fecha" },"dia":{ "$dayOfMonth": "$fecha" },"ano":{ "$year": "$fecha" }}, 
	                         "total": { "$sum": 1 }
	                         } },
	                     { "$sort": { "total": -1 } }
	                   ])
		robot = robots.next()
		objeto_robot = {"cuenta":robot["_id"]["user"],"fecha":str(robot["_id"]["hora"])+":00 "+str(robot["_id"]["ano"])+"-"+str(robot["_id"]["mes"])+"-"+str(robot["_id"]["dia"]),"num_tweets":robot["total"],"imagen":dar_imagen(robot["_id"]["user"])}
	except:
		objeto_robot = {"cuenta":"Info no disponible","fecha":"Info no disponible","num_tweets":"Info no disponible","imagen":"Info no disponible"}
	objeto[user] = objeto_robot
robots_collection.insert(objeto)