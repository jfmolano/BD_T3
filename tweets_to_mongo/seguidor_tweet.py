from pymongo import MongoClient #pip install pymongo
#from datetime import date, datetime, time, timedelta
from datetime import datetime, timedelta

MONGODB_SERVER = "0.0.0.0"
MONGODB_PORT = 27017
MONGODB_DB = "taller3"
TWEETS_COLLECTION = "tweets"
TWEETS_SEGUIDORES = "seguidores"
TWEETS_COLLECTION_CONSULTA = "consulta_seguidores"

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
tweets_collection = db[TWEETS_COLLECTION]
seguidores_collection = db[TWEETS_SEGUIDORES]
consulta_collection = db[TWEETS_COLLECTION_CONSULTA]

objeto_consulta = {}
seguidores = seguidores_collection.find({})
cont_seg = 0
for seguidor in seguidores:
	user = seguidor["username"]
	fechas = seguidor["followersperdate"]
	lista = []
	for f in fechas:
		fecha_str = f.replace("date","")
		fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
		#print fecha
		date_beg_object = fecha
		date_end_object = date_beg_object + timedelta(days=1)
		#print date_end_object
		condicion = {"fecha":{'$lte': date_end_object, '$gte': date_beg_object},"user.screen_name":user,"retweeted_status":{ "$exists": False }}
		tweets = tweets_collection.find(condicion)
		maximo = "No hay actividad"
		maximo_rt = 0
		for t in tweets:
			num_rt = t["retweet_count"]
			if num_rt >= maximo_rt:
				maximo_rt = num_rt
				maximo = t["text"]
		objeto = {"fecha":date_beg_object.strftime("%Y-%m-%d"),"tweet":maximo,"retweets":maximo_rt,"seguidores":seguidor["followersperdate"][f]}
		lista.append(objeto)
	lista = sorted(lista, key=lambda k: k['fecha'])
	lista_2 = []
	seguidores_previos = 0
	i = 0
	for l in lista:
		seguidores_act = l["seguidores"]
		if i == 0:
			delta = 0
		else:
			delta = seguidores_act - seguidores_previos
		l["delta"] = delta
		lista_2.append(l)
		seguidores_previos = seguidores_act
		i = i+1
	objeto_consulta[user] = lista_2
	cont_seg = cont_seg + 1
	print str(cont_seg/69.0*100.0)+" %"
print objeto_consulta
consulta_collection.insert(objeto_consulta)



