import requests 
import collections

SEAT_LIMIT=100

URL="http://127.0.0.1:5000"


movies = []
#Post some movies
try:
	movie = {"name": "Parasite", "date": "03.03.2020", "time": "20:00"}
	response = requests.post((URL+"/movies"), json = movie)
	if response.status_code == 201:
		content = response.json()
		movie["screen_no"] = content["screen_no"]
		movies.append(movie)
	else: raise Exception("First post fails") 	

	movie = {"name": "The Gentlemen", "date": "03.03.2020", "time": "22:15"}	
	response = requests.post((URL+"/movies"), json=movie)
	if response.status_code == 201:
		content = response.json()
		movie["screen_no"] = content["screen_no"]
		movies.append(movie)
	else: raise Exception("Second post fails") 	
	
	for i in range(0,31):
		movie = {"name": "The Gentlemen", "date": '{0:02d}'.format(i+1)+".03.2020", "time": "22:15"}	
		response = requests.post((URL+"/movies"), json=movie)

		if response.status_code == 201:
			content = response.json()
			movie["screen_no"] = content["screen_no"]
			movies.append(movie)
		else: raise Exception("First loop fails") 	
	
	for i in range(0,31):
		movie = {"name": "It must be heaven", "date": '{0:02d}'.format(i+1)+".03.2020", "time": "18:30"}	
		response = requests.post((URL+"/movies"), json=movie)
		if response.status_code == 201:
			content = response.json()
			movie["screen_no"] = content["screen_no"]
			movies.append(movie)
		else: raise Exception("Second loop fails") 	
			
	print ("Test 1 succeeds")		
except Exception as e:
	print(str(e))
	print ("Test 1 fails")


#Check if the movies exist in the D.B.
try:
	if len(movies) < 2:
		raise Exception("Not sufficient for Test 2")
	response = requests.get((URL+"/movies"))
	if response.status_code != 200:
		raise Exception("Unexpected return code")
	result = response.json()
	#del result[0]
	pairs=zip(movies, result)
	if any(x != y for x, y in pairs):
		raise Exception("Result is not equal to local copy")
	print("Test 2 succeeds")
except Exception as e:
	print(str(e))
	print ("Test 2 fails")


#Get non-existing items again
try:
	response = requests.get((URL+"/movies/Gora/01.01.2020"))
	if response.status_code != 404:
		raise Exception("Invalid return code: try1")
	response = requests.get((URL+"/movies/Arog/01.01/2020"))
	if response.status_code != 404:
		raise Exception("Invalid return code: try2")
		
	for movie in movies:
		response = requests.get((URL+"/movies/"+movie["name"]+"/"+movie["date"]))
		if response.status_code != 200:
			raise Exception("Invalid return code (screen no: "+movie["screen_no"]+")")
		if movie not in response.json():
			raise Exception("Reponse does not include test item "+movie["screen_no"])

	print("Test 3 succeeds")
except Exception as e:
	print(str(e))
	print ("Test 3 fails")		
		
#Delete some movies		
try:
	for i in range(10):
		response = requests.delete(URL+"/movies/"+movies[len(movies)-1-i]["name"]+"/"+movies[len(movies)-1-i]["date"])
		if response.status_code != 200:
			raise Exception("Invalid return code in deletion")


	print("Test 4 succeeds")
except Exception as e:
	print(str(e))
	print ("Test 4 fails")			

		
#make reservation to non-existing movies
try:
	for i in range(10):
		response = requests.post((URL+"/ticket"), json=movies[len(movies)-1-i])
		if response.status_code != 404:
			raise Exception("Invalid return code for non existing screen no at /tickets")
	print("Test 5 succeeds")
except Exception as e:
	print(str(e))
	print ("Test 5 fails")	