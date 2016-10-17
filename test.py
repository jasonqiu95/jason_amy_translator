import requests
from flask import Flask, request, Response

KEY = 'EAAQFNW0yLFYBAFh4ZAJr1aIwIRcJxv4WQOv1iz64GP4m6rhZCQqI4p8ZCrIYSb7Rgvoxo2qmU0KM2zL1oG5d9bZAfN1VqN16ragMHKM0eql7f1J6qrT520F3ktBspDfdvXtMuxdM8houekYouTm1hTTOxJZAxeMhLYlXCu0SNaAZDZD'
app = Flask(__name__)


@app.route('/dubhacks', methods=['GET', 'POST'])
def getMessage():
	print "begin"
	myJson = request.json
	print myJson
	try:
		userId = myJson['entry'][0]['messaging'][0]['sender']['id'] 
		print userId
		message = myJson['entry'][0]['messaging'][0]['message']['text']
		print message	
	except KeyError:
		return Response(status=200)

	sendTextMessage(userId, message)

	return Response(status=200)

def sendTextMessage(recipientId, messageText):
	import json
	from translate import Translator
	translation = messageText
	try:
		translator= Translator(to_lang="zh")
		translation = translator.translate(messageText)
	except KeyError:
		pass

	message = json.dumps({"recipient": {"id": recipientId}, "message": {"text": translation}})
	callSendAPI(message, recipientId)

def callSendAPI(messageData, recipientId):
	parameters = {"access_token": KEY, "recipient": recipientId}
	headers = {'Content-type': 'application/json'}
	return requests.post("https://graph.facebook.com/v2.6/me/messages", params=parameters, data=messageData, headers=headers).json()
