import http.client, urllib.parse
import json


def http_call(method, connection, path, dictionary={}):
	
    connection.request( method, path +'?'+ urllib.parse.urlencode(dictionary))
    resp = connection.getresponse()
    status=resp.status
    body_bytes = resp.read()
    body = body_bytes.decode( resp.headers.get_content_charset( 'utf-8' ) )
    return ( status, body )


url = 'maps.googleapis.com'	
connection = http.client.HTTPSConnection(url)

url2='api.mapbox.com'
connection2=http.client.HTTPSConnection(url2)
	

def geoCode(location, typ):
	(status, body ) = http_call( "GET", connection, "/maps/api/geocode/json",{ "key":"AIzaSyCMJmsvDWtXjXaxdsv7FteoCDLUdzHqXXk", "address":location})
	data=json.loads(body)
	#if there are multiple locations
	if len(data["results"])>1 and typ=="coords":
		print ("There is more than one location with that address")
		for i in range (len(data["results"])):
			address=str(i)+" "+data["results"][i]["formatted_address"]
			print (address)
		print ("Enter the list number you would like to use")
		index=input(">>")
		location=data["results"][int(index)]

		if typ=="coords":
			lat=data["results"][int(index)]["geometry"]["location"]["lat"]
			lon=data["results"][int(index)]["geometry"]["location"]["lng"]
			return (lat, lon)

		elif typ=="address":	
			address=data["results"][int(index)]["formatted_address"]
			return (address)
	elif data["status"]=="OK":
		if typ=="coords":
			lat=data["results"][0]["geometry"]["location"]["lat"]
			lon=data["results"][0]["geometry"]["location"]["lng"]
			return (lat, lon)

		else:
			address=data["results"][0]["formatted_address"]
			return (address)
	else:
		print ("Sorry, we could not find that location")
		return (None)



def getDirections(origin, destination):
	googInstructions=""
	otherInstructions=""
	( status, body ) = http_call( "GET", connection, "/maps/api/directions/json",{ "key":"AIzaSyCMJmsvDWtXjXaxdsv7FteoCDLUdzHqXXk", "origin":origin, "destination":destination})
	data=json.loads(body)
	driveTime=data["routes"][0]["legs"][0]["duration"]["text"]
	

	( status, body ) = http_call( "GET", connection, "/maps/api/directions/json",{ "key":"AIzaSyCMJmsvDWtXjXaxdsv7FteoCDLUdzHqXXk", "origin":origin, "mode":"bicycling","destination":destination})
	data=json.loads(body)
	bikeTime=data["routes"][0]["legs"][0]["duration"]["text"]
	#gets directions
	#for i in range (len(data["routes"][0]["legs"][0]["steps"])-1):
	#	googInstructions+=" "+data["routes"][0]["legs"][0]["steps"][i]["html_instructions"]
	#googInstructions=googInstructions.replace('<b>', '')
	#googInstructions=googInstructions.replace('</b>', '')
	#print ("Google Bike Directions : "+googInstructions)

	o=origin.split(',')
	switchedOrigin=o[1]+','+o[0]
	d=destination.split(',')
	switchedDestination=d[1]+','+d[0]

	( status, body ) = http_call( "GET", connection2, "/v4/directions/mapbox.cycling/"+switchedOrigin+";"+switchedDestination+".json", {"access_token":"pk.eyJ1IjoiY2xhdWRpYWZpbm4iLCJhIjoiY2llbHJpMG4xMDBlZHNzbTRud2FubGJtcyJ9.UJaO_S1zju89aeXPex7c9g"})
	data=json.loads(body)
	compTime = (data["routes"][0]["duration"])/60
	
	#gets directions
	#for i in range (len(data["routes"][0]["steps"])):
	#	otherInstructions+=" "+data["routes"][0]["steps"][i]["maneuver"]["instruction"]
	#print("Comparison directions"+str(otherInstructions))
	return (driveTime, bikeTime, compTime)




