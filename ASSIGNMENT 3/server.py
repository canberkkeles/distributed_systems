from flask import Flask, request,jsonify,make_response,Response
from flask_restful import Resource, Api
import auditorium as ad

app = Flask(__name__)
api = Api(app)

AUDITORIUM_COUNT = 10
SEAT_COUNT = 100
RESERVATION_NO = 0
movies = []
moviesWithSeatCount = []
auditoriums = []
reservations = []

for i in range(AUDITORIUM_COUNT):
    auditorium = ad.Auditorium(i)
    auditoriums.append(auditorium)



class Movie(Resource):
    def get(self):
        response = jsonify(movies)
        response.status_code = 200
        return response
    def post(self):
        data = request.get_json()
        movieName = data["name"]
        movieDate = data["date"]
        movieTime = data["time"]
        movieDict = {"name" : movieName, "date" : movieDate, "time" : movieTime}
        availableSeats = []
        for i in range(SEAT_COUNT):
            availableSeats.append(i)
        movieDictWithSeatCount = {"name" : movieName, "date" : movieDate, "time" : movieTime,"available_seats" : availableSeats}

        for a in auditoriums:
            if a.assignNewMovie(movieDate + "@" + movieTime):
                movieDict["screen_no"] = a.auditoriumNo
                movieDictWithSeatCount["screen_no"] = a.auditoriumNo
                movies.append(movieDict)
                moviesWithSeatCount.append(movieDictWithSeatCount)
                return {
                    'screen_no' : a.auditoriumNo
                },201
        return Response(status=404)

class MoviesNew(Resource):
    def get(self,name,date):
        for elt in movies:
            if elt['name'] == name and elt['date'] == date:
                response = jsonify(movies)
                response.status_code = 200 
                return response
    
        response = jsonify(movies)
        response.status_code = 404 
        return response

    def delete(self,name,date):
        for elt in movies:
            if elt['name'] == name and elt['date'] == date:
                movies.remove(elt)
                auditoriumid = elt["screen_no"]
                time = elt["time"]
                auditoriumToUpdate = auditoriums[auditoriumid]
                auditoriumToUpdate.deleteNewMovie(date + "@" + time)
                for r in reservations:
                    if r["name"] == name and r["date"] == date and r["screen_no"] == auditoriumid and r["time"] == time:
                        reservations.remove(r)
                for m in moviesWithSeatCount:
                    if m["name"] == name and m["date"] == date and m["screen_no"] == auditoriumid and m["time"] == time:
                        moviesWithSeatCount.remove(m)

                response = jsonify(movies)
                response.status_code = 200 
                return response
    
        response = jsonify(movies)
        response.status_code = 404 
        return response

class Ticket(Resource):
    def post(self):
        data = request.get_json()
        movieName = data["name"]
        movieDate = data["date"]
        movieTime = data["time"]
        movieScreen = data["screen_no"]

        for elt in moviesWithSeatCount:
            if elt["name"] == movieName and elt["date"] == movieDate and elt["time"] == movieTime and elt["screen_no"] == movieScreen:
                if len(elt["available_seats"]) != 0:
                    seatList = elt["available_seats"]
                    assignedSeat = -1
                    for i in seatList:
                        assignedSeat = i
                        seatList.remove(i)
                        break
                    global RESERVATION_NO
                    RESERVATION_NO += 1
                    reservations.append({"name" : movieName, "date" : movieDate, "time" : movieTime,"screen_no" : movieScreen,"seat_no" :assignedSeat,"reservation_no" : RESERVATION_NO})
                    return{
                        "reservation_no" : RESERVATION_NO
                    },201
                else:
                    return Response(status = 409)
        return Response(status =404)
    def put(self):
        data = request.get_json()
        reservationNo = data["reservation_no"]
        seatNo = data["seat_no"]


        reservationDate = ""
        reservationTime = ""
        reservationName = ""
        reservationScreenNo = -1

        isFound = False
        for r in reservations:
            if r["reservation_no"] == reservationNo:
                reservationDate = r["date"]
                reservationTime = r["time"]
                reservationName = r["name"]
                reservationScreenNo = r["screen_no"]
                isFound = True
        if isFound == False: 
            return Response(status=404)
        
        for elt in moviesWithSeatCount:
            if elt["name"] == reservationName and elt["date"] == reservationDate and elt["time"] == reservationTime and elt["screen_no"] == reservationScreenNo:
                seatList = elt["available_seats"]
                if seatNo not in seatList:
                    return Response(status= 409)
                else:
                    """
                    currSeat = reservations[reservationNo]["seat_no"]
                    reservations[reservationNo]["seat_no"] = seatNo
                    reservations[reservationNo]["available_seats"].append(currSeat)
                    """

                    for r in reservations:
                        if r["reservation_no"] == reservationNo:
                            currSNo = r["seat_no"]
                            r["seat_no"] = seatNo
                            elt["available_seats"].append(currSNo)





                    return Response(status = 200)

    
    def delete(self):
        data = request.get_json()
        reservationNo = data["reservation_no"]

        for r in reservations:
            if r["reservation_no"] == reservationNo:
                reservationDate = r["date"]
                reservationTime = r["time"]
                reservationName = r["name"]
                reservationScreenNo = r["screen_no"]

                for elt in moviesWithSeatCount:
                    if elt["name"] == reservationName and elt["date"] == reservationDate and elt["time"] == reservationTime and elt["screen_no"] == reservationScreenNo:
                        elt["available_seats"].append(r["seat_no"])
                        break
                reservations.remove(r)
                return Response(status=200)
        return Response(status=404)

    def get(self):
        if not request.data:
                
            response = jsonify(reservations)
            response.status_code = 200
            return response

        for res in reservations:
            if request.get_json()['reservation_no'] == res['reservation_no']:
                return{
                        "name" : res['name'],
                        "date" : res['date'],
                        "time" : res['time'],
                        "screen_no" : res['screen_no'],
                        "seat_no" : res['seat_no']
                    }, 200 
        response = jsonify(movies)
        response.status_code = 404 
        return response


            


api.add_resource(Movie,"/movies")
api.add_resource(MoviesNew, "/movies/<string:name>/<string:date>")
api.add_resource(Ticket,"/ticket")


if __name__ == '__main__':
    app.run(debug=True)


