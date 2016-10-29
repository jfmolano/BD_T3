
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin
import csv
from pymongo import MongoClient #pip install pymongo
from bson.json_util import dumps
import json

MONGODB_SERVER = "0.0.0.0"
MONGODB_PORT = 27017
MONGODB_DB = "taller3"
TWEETS_COLLECTION = "tweets"
CONSULTA_SEG = "consulta_seguidores"
CONSULTA_ROB = "consulta_robots"


connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
tweets_collection = db[TWEETS_COLLECTION]
seguidores_collection = db[CONSULTA_SEG]
robots_collection = db[CONSULTA_ROB]

app = Flask(__name__)
CORS(app)

marcas = [
    {
        'Id': u'1',
        'Dato': u'A'
    },
    {
        'Id': u'2',
        'Dato': u'B'
    }
]

@app.route('/api/marcas', methods=['GET'])
def get_marcas():
	return jsonify({'marcas': marcas})

@app.route('/api/dar_marca', methods=['POST'])
def dar_marca_post():
	if not request.json or not 'Id' in request.json:
		abort(400)
	marca = {
	'Id': request.json['Id'],
	'Dato': request.json.get('Dato', "")
	}
	return jsonify({'marca': marca}), 201

@app.route('/api/dar_marca/<Id>/<Dato>', methods=['GET'])
def dar_marca_get(Id,Dato):
	marca = {
	'Id': Id,
	'Dato': Dato
	}
	return jsonify({'marca': marca}), 201

@app.route('/consulta1', methods=['GET'])
def consulta1():
	print "Entra a servicio"
	resultado = tweets_collection.aggregate([
                     { "$group": { 
                         "_id": "$user.screen_name", 
                         "total": { "$sum": 1 },
                         "promedio_RT": { "$avg": "$retweet_count" },
                         "promedio_seguidores": { "$avg": "$user.followers_count" }
                         } },
                         { "$match" : {"total": {"$gt":3000}}},
                     { "$sort": { "total": -1 } }
                   ])
	#resultado = tweets_collection.find()
	l = list(resultado)
	lista_nombres = []
	objeto = {}
	for i in l:
		item = {}
		item["promedio_RT"] = '%.2f' % i["promedio_RT"]
		item["promedio_seguidores"] = '%.2f' % i["promedio_seguidores"]
		item["relacion"] = (i["promedio_RT"]/(i["promedio_seguidores"]+0.0))
		objeto[i["_id"]] = item
		lista_nombres.append(i["_id"])

	return dumps({"objeto":objeto,"lista":lista_nombres}), 201

@app.route('/consulta2', methods=['GET'])
def consulta2():
	print "Entra a servicio"
	resultado = tweets_collection.aggregate([
                     { "$group": { 
                         "_id": "$user.screen_name", 
                         "total": { "$sum": 1 },
                         "promedio_RT": { "$avg": "$retweet_count" },
                         "promedio_tuits": { "$avg": "$user.statuses_count" }
                         } },
                         { "$match" : {"total": {"$gt":3000}}},
                     { "$sort": { "total": -1 } }
                   ])
	#resultado = tweets_collection.find()
	l = list(resultado)
	lista_nombres = []
	objeto = {}
	for i in l:
		item = {}
		item["promedio_RT"] = '%.2f' % i["promedio_RT"]
		item["promedio_tuits"] = '%.2f' % i["promedio_tuits"]
		item["relacion"] = (i["promedio_RT"]/(i["promedio_tuits"]+0.0))
		objeto[i["_id"]] = item
		lista_nombres.append(i["_id"])

	return dumps({"objeto":objeto,"lista":lista_nombres}), 201

@app.route('/consulta3', methods=['GET'])
def consulta3():
	print "Entra a servicio"
	resultado = tweets_collection.aggregate([
                     { "$group": { 
                         "_id": "$user.screen_name", 
                         "total": { "$sum": 1 },
                         "promedio_favs": { "$avg": "$user.favourites_count" },
                         "promedio_faveado": { "$avg": "$favorite_count" }
                         } },
                         { "$match" : {"total": {"$gt":3000}}},
                     { "$sort": { "total": -1 } }
                   ])
	#resultado = tweets_collection.find()
	l = list(resultado)
	lista_nombres = []
	objeto = {}
	for i in l:
		item = {}
		item["promedio_favs"] = '%.2f' % i["promedio_favs"]
		item["promedio_faveado"] = '%.2f' % i["promedio_faveado"]
		item["relacion"] = (i["promedio_faveado"]/(i["promedio_favs"]+0.0))
		objeto[i["_id"]] = item
		lista_nombres.append(i["_id"])

	return dumps({"objeto":objeto,"lista":lista_nombres}), 201

@app.route('/consulta_seguidores', methods=['GET'])
def consulta_seguidores():
	print "Entra a servicio"
	resultado = seguidores_collection.find()
	l = list(resultado)
	return dumps(l), 201

@app.route('/consulta_robots', methods=['GET'])
def consulta_robots():
	print "Entra a servicio"
	resultado = robots_collection.find()
	l = list(resultado)
	return dumps(l), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=8080)