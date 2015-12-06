import http.client, urllib.parse
import json
import GoogleDirections


def http_call(method, connection, path, dictionary={}):
	
    connection.request( method, path +'?'+ urllib.parse.urlencode(dictionary))
    resp = connection.getresponse()
    status=resp.status
    body_bytes = resp.read()
    body = body_bytes.decode( resp.headers.get_content_charset( 'utf-8' ) )
    return ( status, body )


url = 'www.eventbriteapi.com'	
connection = http.client.HTTPSConnection(url)

categories={}

def getInfo(data, origin):
	x=len(data["events"])
	if x>0:
		for i in range (x):
			venue_id=data["events"][i]["venue_id"]
			category_id=data["events"][i]["category_id"]
			catName=getCategoryInfo(category_id)
			venInfo=getVenueInfo(venue_id)
			venName=venInfo[0]
			venCoords=venInfo[1]
			venAdd=venInfo[2]
			drivingtime=GoogleDirections.getDirections(origin, venCoords)
			startdate=data["events"][i]["start"]["local"].split('T')
			enddate=data["events"][i]["end"]["local"].split('T')
			print ()
			print(str(i+1) +" : "+data["events"][i]["name"]["text"])
			print("Venue  : "+venName)
			print("Address : "+venAdd)
			print("Start Date : "+startdate[0])
			print("Start Time : "+startdate[1])
			if startdate[0]!=enddate[0]:
				print("End Date : "+enddate[0])
			print("End Time : "+enddate[1])
			print("Driving Time : "+drivingtime[0])
			print ("Biking Time : "+drivingtime[1])
			print ("Comparison Time :"+str(drivingtime[2])+"mins")
			print("Link : "+data["events"][i]["url"])
	else:
		print ("There are no events available")

#returns venue name and coordinates
def getVenueInfo(venue_id):
	( status, body ) = http_call( "GET", connection, "/v3/venues/"+venue_id+"/", {"token":"6YDDAPKWBOWBGAGGSFNW"})
	venData=json.loads(body)
	venAdd=""
	venName=venData["name"]
	if venData["address"]["address_1"] != None:
		venAdd+=venData["address"]["address_1"]
	if venData["address"]["city"] != None:
		venAdd+=venData["address"]["city"]
	else:
		venAdd="Address not available"
	venLat=venData["address"]["latitude"]
	venLon=venData["address"]["longitude"]
	latlon=str(venLat)+","+str(venLon)
	if venName != None:
		return (venName, latlon, venAdd)	
		
	else:
		return ("",latlon, venAdd)		

#return category name
def getCategoryInfo(category_id):
	if category_id != None:
		if category_id not in categories:
			( status, body ) = http_call( "GET", connection, "/v3/categories/"+category_id+"/", {"token":"6YDDAPKWBOWBGAGGSFNW"})
			catData=json.loads(body)
			catName=catData["name"]
			categories[category_id]=catName
		else:
			catName=categories[category_id]
		return catName
	else:
		return ""


