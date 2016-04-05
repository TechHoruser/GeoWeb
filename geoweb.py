__author__ = 'Jos\'user'
import twitter
import io
import json
import datetime

from datetime import timedelta
from flask import Flask, request, render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map


#Funcion para la conexion.
def oauth_login():
    CONSUMER_KEY = 'olCGavekol2fbLebHRejjaoR6'
    CONSUMER_SECRET = 'Ht9iRfXzh3mXr0994zLuCSGZHZc5mMvhddNqhP8yjS6a5Qhb3u'
    OAUTH_TOKEN = '722369984-8cG7gCQxWL6cCJHstWAZCQ1ADz2LdNjLs38EpEjw'
    OAUTH_TOKEN_SECRET = 'KNkkFKjZy6QMJKA5yTLb6e8BLjGwnrAqqkBGNs7Oji4Nu'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def geo(tw,ht):
    query = tw.search.tweets(q=('#'+ht),count=100)
    
    listado=[]
    
    for resultado in query["statuses"]:
        # only process a result if it has a geolocation
        if resultado["place"]:
            #(resultado["place"]["bounding_box"]["coordinates"][0])
            momento = datetime.datetime.strptime(resultado["created_at"], '%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=1)
            latitud = 0
            longitud = 0
            for e in resultado["place"]["bounding_box"]["coordinates"][0]:
                latitud += e[0]
                longitud += e[1]
            latitud = latitud/len(resultado["place"]["bounding_box"]["coordinates"][0])
            longitud = longitud/len(resultado["place"]["bounding_box"]["coordinates"][0])
            
            momento = momento + datetime.timedelta(hours=1)
            listado.append({"id":resultado["id"], "lugar" : resultado["place"]["full_name"], "momento" : momento, "latitud" : latitud, "longitud" : longitud, "usuario":resultado["user"]})
            
    return listado

def tagMethod(tag):
	listado = geo(oauth_login(),tag)
	l={}

	for e in listado:
		l.update({e['usuario']['profile_image_url']:[(e['longitud'],e['latitud'])]})

	mapa = Map(
		identifier="view-side",
		lat=40.3450396,
		lng=-3.6517684,
		zoom=6,
		markers=l,
		style="height:600px;width:800px;margin:0;"
	)

	return render_template('tag.html', mapa=mapa, tag=tag, listado=listado)




app = Flask(__name__)
GoogleMaps(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tag/<tag>')
def tag1(tag):
	return tagMethod(tag)
	
@app.route('/tag/', methods=['POST'])
def tag2():
	return tagMethod(request.form['tag'])


if __name__ == "__main__":
    app.run(debug=True)



