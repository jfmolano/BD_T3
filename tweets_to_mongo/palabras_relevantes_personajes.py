from pymongo import MongoClient #pip install pymongo

MONGODB_SERVER = "0.0.0.0"
MONGODB_PORT = 27017
MONGODB_DB = "taller3"
TWEETS_COLLECTION = "tweets"
WC_USER_COLLECTION = "word_count_user"
CONSULTA_PALABRAS_US_COLLECTION = "consulta_palabras_usuario"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
tweets_collection = db[TWEETS_COLLECTION]
wc_user_collection = db[WC_USER_COLLECTION]
palabras_us_collection = db[CONSULTA_PALABRAS_US_COLLECTION]

usuarios = tweets_collection.aggregate([
                     { "$group": { 
                         "_id": "$user.screen_name", 
                         "total": { "$sum": 1 }
                         } },
                     { "$match": { "total": {"$gt":3000} } }
                   ])

objeto = {}
for usuario in usuarios:
	user = usuario["_id"]
	print user
	palabras =  wc_user_collection.find({"_id.usuario":user}).sort("value",-1).limit(10)
	lista = []
	for palabra in palabras:
		if palabra["_id"]["palabra"] != ("@"+user.lower()):
			lista.append({"palabra":palabra["_id"]["palabra"],"cuenta":palabra["value"]})
	objeto[user] = lista
print objeto
palabras_us_collection.insert(objeto)