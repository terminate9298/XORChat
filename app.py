from flask import Flask , request , jsonify , render_template , redirect , url_for, send_file, session
from flask_socketio import SocketIO, send, emit , join_room, leave_room
import time
import pyrebase
from utils import ParellelDB

firebaseConfig = {
	'apiKey': "APIKey Here",
	'authDomain': "Authentication Domain",
	'databaseURL': "URL",
	'projectId': "Project ID",
	'storageBucket': "Bucket Name",
	'messagingSenderId': "Sender ID",
	'appId': "APP ID",
	'measurementId': "Other ID"
}

#Copy you Firebase Configurations in firebaseConfig
db = ParellelDB()
db.set_FireConfig(firebaseConfig)
db.start()
db.get_rooms()
# firebase = pyrebase.initialize_app(firebaseConfig)
# db = firebase.database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdsasasdsadafdsagnbwevvdvs'
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True

socketio = SocketIO(app)

# rooms = []

# rooms = db.child('PgPlFFm5ZEv5FPT022aOnT9W9xkWZMGJ').get().val().values()
# rooms = list(rooms)
# print(rooms)

@socketio.on('join' )
def handleConnect(resp):
	data = {
		"user" : resp['username'],
		"class" :"success",
		"time" : str(time.ctime(time.time())),
		"message" : 'Joined The Group Chat'
	}

	join_room(resp['room'].lower())
	if(resp['new'] == 'true'):
		emit('alert' , data , room = resp['room'])
	# else:
	# 	data['message'] = 'Reconnected ....'
	# 	data['class'] = 'info'
	# 	emit('alert' , data)
	

@socketio.on('message')
def handleMessage(msg):
	if msg['message'] != "":
		# msg["class"] = ""
		msg["time"] = str(time.ctime(time.time()))
		db.insert_child(msg['room'], msg)
		emit('message' , msg , room = msg['room'])
		# emit('alert' , msg , room = msg['room'])

@socketio.on('leave')
def handleDisconnect(resp):

	data = {"user": resp['username'],
			"class": "warning",
			"time": str(time.ctime(time.time())),
			"message": 'Left The Group Chat'
			}
	leave_room(resp['room'].lower())
	emit('alert', data, room = resp['room'].lower())


@app.route('/<room>')
def chat(room):
	room = room.lower()
	to = db.return_room_data(room)
	# print(to)
	return render_template('chat.html' , data = to)

@app.route('/')
def main():
	return render_template('index.html')

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

if __name__ == '__main__':
	socketio.run(app)
	# app.run(debug = True)