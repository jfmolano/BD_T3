from pymongo import MongoClient
import json
import urllib2

client = MongoClient('localhost', 27017)
db = client['taller3']
collection_tweets = db['tweets']
collection_seguidores = db['seguidores']
lista_id = collection_tweets.distinct("user.id")
lista_actual = collection_seguidores.distinct("username")
conjunto_actual = set(lista_actual)
for id_user in lista_id:
	try:
		api = urllib2.urlopen("http://api.twittercounter.com/?apikey=e9335031a759f251ee9b4e2e6634e1c5&twitter_id="+str(id_user)).read()
	except:
		print "api error"
	obj = eval(api)
	if obj["username"] in conjunto_actual:
		print "Seguidores ya en BD"
	else:
		print obj
		collection_seguidores.insert(obj)
