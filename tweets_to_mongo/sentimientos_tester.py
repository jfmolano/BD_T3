import nltk
from pymongo import MongoClient
from random import randint

def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

client = MongoClient('localhost', 27017)
db = client['taller3']
collection_tweets = db['tweets']
collection_clasificador = db['clasificador_manual']

conjunto_entrenamiento = 200

tuits_positivos = collection_clasificador.find({"sentiment":"positive"}).limit(conjunto_entrenamiento)
tuits_negativos = collection_clasificador.find({"sentiment":"negative"}).limit(conjunto_entrenamiento)

tuits_positivos_test = collection_clasificador.find({"sentiment":"positive"}).skip(conjunto_entrenamiento)
tuits_negativos_test = collection_clasificador.find({"sentiment":"negative"}).skip(conjunto_entrenamiento)
tuits_neutrales_test = collection_clasificador.find({"sentiment":"neutral"}).limit(93)

pos_tweets = []
neg_tweets = []

for item in tuits_positivos:
	pos_tweets.append((item["text"],"positive"))

for item in tuits_negativos:
	pos_tweets.append((item["text"],"negative"))

#Tomado de: http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/

tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
	words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
	tweets.append((words_filtered, sentiment))

print tweets

word_features = get_word_features(get_words_in_tweets(tweets))

print word_features

training_set = nltk.classify.apply_features(extract_features, tweets)

print training_set

classifier = nltk.NaiveBayesClassifier.train(training_set)

print classifier.show_most_informative_features(32)

positivo_positivo = 0
positivo_neutro = 0
positivo_negativo = 0
negativo_positivo = 0
negativo_neutro = 0
negativo_negativo = 0
neutro_positivo = 0
neutro_neutro = 0
neutro_negativo = 0

for t in tuits_positivos_test:
	#print t
	positivo = classifier.prob_classify(extract_features(t["text"].split())).prob("positive")
	negativo = classifier.prob_classify(extract_features(t["text"].split())).prob("negative")
	if positivo > 0.65:
		positivo_positivo = positivo_positivo + 1
	elif positivo <= 0.65 and positivo > 0.50:
		positivo_neutro = positivo_neutro + 1
	else:
		positivo_negativo = positivo_negativo + 1

for t in tuits_negativos_test:
	positivo = classifier.prob_classify(extract_features(t["text"].split())).prob("positive")
	negativo = classifier.prob_classify(extract_features(t["text"].split())).prob("negative")
	if positivo > 0.65:
		negativo_positivo = negativo_positivo + 1
	elif positivo <= 0.65 and positivo > 0.50:
		negativo_neutro = negativo_neutro + 1
	else:
		negativo_negativo = negativo_negativo + 1

for t in tuits_neutrales_test:
	#print "neutro"
	positivo = classifier.prob_classify(extract_features(t["text"].split())).prob("positive")
	negativo = classifier.prob_classify(extract_features(t["text"].split())).prob("negative")
	if positivo > 0.65:
		neutro_positivo = neutro_positivo + 1
	elif positivo <= 0.65 and positivo > 0.45:
		neutro_neutro = neutro_neutro + 1
	else:
		neutro_negativo = neutro_negativo + 1

print "positivo_positivo " + str(positivo_positivo)
print "positivo_neutro " + str(positivo_neutro)
print "positivo_negativo " + str(positivo_negativo)
print "negativo_positivo " + str(negativo_positivo)
print "negativo_neutro " + str(negativo_neutro)
print "negativo_negativo " + str(negativo_negativo)
print "neutro_positivo " + str(neutro_positivo)
print "neutro_neutro " + str(neutro_neutro)
print "neutro_negativo " + str(neutro_negativo)

matriz = [[positivo_positivo,positivo_neutro,positivo_negativo],
			[neutro_positivo,neutro_neutro,neutro_negativo],
			[negativo_positivo,negativo_neutro,negativo_negativo]]

print matriz