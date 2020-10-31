from threading import Thread
import pyrebase
import time
class ParellelDB(Thread):
	def __init__(self):
		super(ParellelDB , self).__init__()
		self.daemon = True

	def set_FireConfig(self , config):
		self.config = config

	def run(self):
		self.firebase = pyrebase.initialize_app(self.config)
		self.db = self.firebase.database()

	def get_rooms(self):
		self.rooms = self.db.child('rooms').get().val().keys()
		self.rooms = list(self.rooms)
		# return self.rooms

	def insert_child(self, key , value):
		self.db.child('rooms').child(key).push(value)
		
	def return_room_data(self , room ):
		if room in self.rooms:
			return self.db.child('rooms').child(room).get().val().values()
		else:
			msg = {'message':'New Room Created . Welcome to your New Room','room':room,'time':str(time.ctime(time.time())),'user':'Admin'}
			self.insert_child(room , msg)
			self.rooms.append(room)
			return [msg]
