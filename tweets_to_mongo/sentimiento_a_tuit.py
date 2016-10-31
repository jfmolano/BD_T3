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
collection_tweets_sentimiento = db['tweets_sentimiento']
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

tweets_l = collection_tweets.find({})
i = 0
for tweet in tweets_l:
	positivo = classifier.prob_classify(extract_features(tweet["text"].split())).prob("positive")
	negativo = classifier.prob_classify(extract_features(tweet["text"].split())).prob("negative")
	sentimiento = ""
	if positivo > 0.65:
		sentimiento = "positive"
	elif positivo <= 0.65 and positivo > 0.50:
		sentimiento = "neutral"
	else:
		sentimiento = "negative"
	tweet["sentimiento"] = sentimiento
	collection_tweets_sentimiento.insert(tweet)
	print str(i/(361818.0)*100.0)+" %"
	i = i+1