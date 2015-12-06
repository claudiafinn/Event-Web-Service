import sqlite3
import json

class EventData:
	db='events_db.sqlite'
	conn = sqlite3.connect(db)
	c = conn.cursor()

	c.execute('''CREATE TABLE IF NOT EXISTS Events
             (name TEXT PRIMARY KEY, location TEXT, date TEXT, time TEXT, category TEXT, travel_time TEXT)''')
	
	my_data=None

	def __init__(self, data):
		self.my_data=data
		self.fuckWithData()

	def fuckWithData(self):
		x=len(self.my_data["events"])
		for i in range (x):
			name=self.my_data["events"[i]["name"]
			start=self.my_data["events"[i]["start"]["local"]
			venue_id=self.my_data["events"[i]["venue_id"]
			category_id=self.my_data["events"[i]["category_id"]
			self.c.execute("INSERT OR REPLACE INTO Warehouse VALUES(?,?,?,?)", 
			(key, int(data[key])))
