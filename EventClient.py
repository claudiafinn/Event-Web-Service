import http.client, urllib.parse
import json
import GoogleDirections, Eventbrite, BandsinTown
import datetime


def http_call(method, connection, path, dictionary={}):
	
    connection.request( method, path +'?'+ urllib.parse.urlencode(dictionary))
    resp = connection.getresponse()
    status=resp.status
    body_bytes = resp.read()
    body = body_bytes.decode( resp.headers.get_content_charset( 'utf-8' ) )
    return ( status, body )

date=datetime.date.today()

print("Welcome to Claudia's Event App")
print("What's your location?")
origin=input(">>")
print("How far are you willing to travel? (miles)")
distance=input(">>")
try:
	distance=int(distance)
except:
	print ("Not a number")
	exit()
if distance>150:
	distance=150
print("What is your time frame? (today, tomorrow, this week)")
timeframe=input(">>")

def getDate(x):
	date2=date+datetime.timedelta(days=x)
	bandTimeFrame = str(date)+","+str(date2)
	return bandTimeFrame
	
if timeframe == "today":
	bandTimeFrame=getDate(0)
elif timeframe == "tomorrow":
	bandTimeFrame=getDate(1)
elif timeframe == "this week":
	day=date.isoweekday()
	timeframe="this_week"
	bandTimeFrame=getDate(7-day)
else:
	print ("Bad time request")
	quit()
latlon=GoogleDirections.geoCode(origin, "coords")
if latlon==None:
	exit()
else:
	lat=latlon[0]
	lon=latlon[1]
	origin=str(lat)+','+str(lon)


url = 'www.eventbriteapi.com'	
connection = http.client.HTTPSConnection(url)
( status, body ) = http_call( "GET", connection, "/v3/events/search/", {"location.address":origin,"location.within":str(distance)+"mi", "start_date.keyword":timeframe,"sort_by":"date","token":"6YDDAPKWBOWBGAGGSFNW"})
data=json.loads(body)

url = 'api.bandsintown.com'	
connection = http.client.HTTPConnection(url)
( status, body ) = http_call( "GET", connection, "/events/search/", {"date": bandTimeFrame, "format":"json","location":str(lat)+","+str(lon),"radius":str(distance), "app_id":"claudiasapp"})
data2=json.loads(body)

count=len(data["events"])+len(data2)
print ("We found #"+str(count)+ " events")
Eventbrite.getInfo(data, origin)
BandsinTown.getInfo(data2, origin, len(data["events"]))

