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


url = 'api.bandsintown.com'	
connection = http.client.HTTPConnection(url)

def getInfo(data, origin, num):
	x=len(data)
	#if data["errors"]:
	#	print ("Oh no, there was an error" + data["errors"])
	
	if x>0 :
		for i in range (x):
			lat = data[i]["venue"]["latitude"]
			lon =data[i]["venue"]["longitude"]
			times=GoogleDirections.getDirections(origin, str(lat)+","+str(lon))
			venAddress=GoogleDirections.geoCode(str(lat)+","+str(lon), "address")
			printData(data, i, times, num+i, venAddress)
	else:
		print ("No Events Available")
		
def printData(data, i, times, num, address):
	print ()
	print(str(num+1)+" : "+data[i]["artists"][0]["name"])
	print("Venue : "+data[i]["venue"]["name"])
	print ("Address : "+address)
	datetime= data[i]["datetime"].split('T')
	date=datetime[0]
	time=datetime[1]
	print ("Date : "+date )
	print ("Time : "+time )
	print("Driving time : "+times[0])
	print ("Biking time : "+times[1])
	print("Comparison biking time "+str(times[2])+"mins")	
	print ("Ticket status : "+data[i]["ticket_status"])
	print("Link : "+data[i]["ticket_url"])

