from datetime import datetime
from datetime import timedelta

def splitDate(d):
	dateAndHour = d.split("@")
	fullDate = dateAndHour[0]
	fullHour = dateAndHour[1]

	dayMonthYear = fullDate.split(".")

	dayWithProbZero   = dayMonthYear[0]
	monthWithProbZero = dayMonthYear[1]

	if dayWithProbZero[0] == '0':
		dayWithProbZero = dayWithProbZero[1]

	if monthWithProbZero[0] == '0':
		monthWithProbZero = monthWithProbZero[1]
	
	day   = int(dayWithProbZero)
	month = int(monthWithProbZero)
	year  = int(dayMonthYear[2])

	minuteHour = fullHour.split(":")
	hour = int(minuteHour[0])
	minute = int(minuteHour[1])

	return day,month,year,hour,minute

def formatDate(d):
	# THIS FUNCTION TAKES d AS datetime BUT IT INTERPRET IT AS A STRING, THAT IS AN ERROR
	# HOPE SOMEDAY SOMEONE WILL HELP ME FIX THIS :)
	day   = str(d.day)
	month = str(d.month)
	year = str(d.year)
	hour = str(d.hour)
	minute = str(d.minute)

	return day + "." + month + "." + year + "@" + hour + ":" + minute


class Auditorium:
	def __init__(self,auditoriumNo,assignedDates = list()):
		self.auditoriumNo = auditoriumNo
		self.assignedDates = assignedDates

	def assignNewMovie(self,movieDate):
		if len(self.assignedDates) == 0:
			day,month,year,hour,minute = splitDate(movieDate)
			dToAdd = datetime(year,month,day,hour,minute)
			self.assignedDates.append(dToAdd)
			return True
		else:
			for d in (self.assignedDates):
				# FOR CURRENT ASSIGNED MOVIE
				d = datetime(d.year,d.month,d.day,d.hour,d.minute)
				day,month,year,hour,minute = splitDate(formatDate(d)) 
				assignedMovieDate = datetime(year,month,day,hour,minute)

				# FOR NEWLY ASSIGNED MOVIE
				currDay,currMonth,curYear,currHour,currMinute = splitDate(movieDate)
				currMovieDate = datetime(curYear,currMonth,currDay,currHour,currMinute)

				if (assignedMovieDate + timedelta(hours = 2) <= currMovieDate) or (assignedMovieDate - timedelta(hours=2) >= currMovieDate):

					day,month,year,hour,minute = splitDate(formatDate(currMovieDate))
					dToAdd = datetime(year,month,day,hour,minute)
					self.assignedDates.append(dToAdd)
					return True
			return False

	def deleteNewMovie(self,movieDate):
		for d in (self.assignedDates):
			day,month,year,hour,minute = splitDate(movieDate)
			dToRemove = datetime(year,month,day,hour,minute)
			if dToRemove == d:
				self.assignedDates.remove(dToRemove)








				






				


