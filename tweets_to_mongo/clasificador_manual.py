#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from pymongo import MongoClient
from random import randint

client = MongoClient('localhost', 27017)
db = client['taller3']
collection_tweets = db['tweets']
collection_clasificador = db['clasificador_manual']

cursor = collection_tweets.find()
cuenta = cursor.count()
print cursor
while True:
	texto = cursor[randint(0,cuenta)]["text"]
	print texto
	polaridad = raw_input("")
	if polaridad == "s":
		collection_clasificador.insert({"text":texto,"sentiment":"positive"})
	elif polaridad == "n":
		collection_clasificador.insert({"text":texto,"sentiment":"negative"})
	else:
		collection_clasificador.insert({"text":texto,"sentiment":"neutral"})