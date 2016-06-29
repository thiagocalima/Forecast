from datetime import datetime
import urllib.request
import urllib
import json
import sys
from datetime import datetime
import re
import smtplib

class Weather(object):
    def __init__(self, id, main, description, icon):
        self.id = id
        self.main = main
        self.description = description
        self.icon = icon


class Main(object):
    def __init__(self, temp, temp_min, temp_max, pressure, sea_level, grnd_level, humidity, temp_kf):
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.sea_level = sea_level
        self.grnd_level = grnd_level
        self.humidity = humidity
        self.temp_kf = temp_kf


class List(object):
    def __init__(self, dt, main, weather, clouds, wind, sys, dt_txt, rain = None):
        self.dt = dt
        self.main = main
        self.weather = []
        for element in weather:
            self.weather.append(Weather(**element))
        self.clouds = clouds
        self.wind = wind
        self.rain = rain
        self.sys = sys
        self.dt_txt = dt_txt


class Coord(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


class City(object):
    def __init__(self, id, name, coord, country, population):
        self.id = id
        self.name = name
        self.coord = Coord(**coord)
        self.country = country
        self.population = population
        

class Forecast(object):
    def __init__(self, cod, message, city, cnt, list):
        self.cod = cod
        self.message = message
        self.city = City(**city)
        self.cnt = cnt
        self.list = []
        for element in list:
            self.list.append(List(**element))


class Place(object):
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord


class Reason(object):
    def __init__(self, id, category, description, good):
        self.id = id
        self.category = category
        self.description = description
        self.good = good


def urlBuilder(coord):
    return "http://api.openweathermap.org/data/2.5/forecast?lat=" + coord.lat + "&lon=" + coord.lon + ""


def reasonsBuilder():
    reasons = []
    reasonList = [{"id":200,"category":"Thunderstorm","description":"thunderstorm with light rain","good":0},{"id":201,"category":"Thunderstorm","description":"thunderstorm with rain","good":0},{"id":202,"category":"Thunderstorm","description":"thunderstorm with heavy rain","good":0},{"id":210,"category":"Thunderstorm","description":"light thunderstorm","good":0},{"id":211,"category":"Thunderstorm","description":"thunderstorm","good":0},{"id":212,"category":"Thunderstorm","description":"heavy thunderstorm","good":0},{"id":221,"category":"Thunderstorm","description":"ragged thunderstorm","good":0},{"id":230,"category":"Thunderstorm","description":"thunderstorm with light drizzle","good":0},{"id":231,"category":"Thunderstorm","description":"thunderstorm with drizzle","good":0},{"id":232,"category":"Thunderstorm","description":"thunderstorm with heavy drizzle","good":0},{"id":300,"category":"Drizzle","description":"light intensity drizzle","good":0},{"id":301,"category":"Drizzle","description":"drizzle","good":0},{"id":302,"category":"Drizzle","description":"heavy intensity drizzle","good":0},{"id":310,"category":"Drizzle","description":"light intensity drizzle rain","good":0},{"id":311,"category":"Drizzle","description":"drizzle rain","good":0},{"id":312,"category":"Drizzle","description":"heavy intensity drizzle rain","good":0},{"id":313,"category":"Drizzle","description":"shower rain and drizzle","good":0},{"id":314,"category":"Drizzle","description":"heavy shower rain and drizzle","good":0},{"id":321,"category":"Drizzle","description":"shower drizzle","good":0},{"id":500,"category":"Rain","description":"light rain","good":0},{"id":501,"category":"Rain","description":"moderate rain","good":0},{"id":502,"category":"Rain","description":"heavy intensity rain","good":0},{"id":503,"category":"Rain","description":"very heavy rain","good":0},{"id":504,"category":"Rain","description":"extreme rain","good":0},{"id":511,"category":"Rain","description":"freezing rain","good":0},{"id":520,"category":"Rain","description":"light intensity shower rain","good":0},{"id":521,"category":"Rain","description":"shower rain","good":0},{"id":522,"category":"Rain","description":"heavy intensity shower rain","good":0},{"id":531,"category":"Rain","description":"ragged shower rain","good":0},{"id":600,"category":"Snow","description":"light snow","good":0},{"id":601,"category":"Snow","description":"snow","good":0},{"id":602,"category":"Snow","description":"heavy snow","good":0},{"id":611,"category":"Snow","description":"sleet","good":0},{"id":612,"category":"Snow","description":"shower sleet","good":0},{"id":615,"category":"Snow","description":"light rain and snow","good":0},{"id":616,"category":"Snow","description":"rain and snow","good":0},{"id":620,"category":"Snow","description":"light shower snow","good":0},{"id":621,"category":"Snow","description":"shower snow","good":0},{"id":622,"category":"Snow","description":"heavy shower snow","good":0},{"id":701,"category":"Atmosphere","description":"mist","good":0},{"id":711,"category":"Atmosphere","description":"smoke","good":0},{"id":721,"category":"Atmosphere","description":"haze","good":0},{"id":731,"category":"Atmosphere","description":"sand, dust whirls","good":0},{"id":741,"category":"Atmosphere","description":"fog","good":0},{"id":751,"category":"Atmosphere","description":"sand","good":0},{"id":761,"category":"Atmosphere","description":"dust","good":0},{"id":762,"category":"Atmosphere","description":"volcanic ash","good":0},{"id":771,"category":"Atmosphere","description":"squalls","good":0},{"id":781,"category":"Atmosphere","description":"tornado","good":0},{"id":800,"category":"Clouds","description":"clear sky","good":1},{"id":801,"category":"Clouds","description":"few clouds","good":1},{"id":802,"category":"Clouds","description":"scattered clouds","good":1},{"id":803,"category":"Clouds","description":"broken clouds","good":1},{"id":804,"category":"Clouds","description":"overcast clouds","good":1},{"id":900,"category":"Extreme","description":"tornado","good":0},{"id":901,"category":"Extreme","description":"tropical storm","good":0},{"id":902,"category":"Extreme","description":"hurricane","good":0},{"id":903,"category":"Extreme","description":"cold","good":0},{"id":904,"category":"Extreme","description":"hot","good":0},{"id":905,"category":"Extreme","description":"windy","good":0},{"id":906,"category":"Extreme","description":"hail","good":0},{"id":951,"category":"Additional","description":"calm","good":1},{"id":952,"category":"Additional","description":"light breeze","good":1},{"id":953,"category":"Additional","description":"gentle breeze","good":1},{"id":954,"category":"Additional","description":"moderate breeze","good":1},{"id":955,"category":"Additional","description":"fresh breeze","good":1},{"id":956,"category":"Additional","description":"strong breeze","good":1},{"id":957,"category":"Additional","description":"high wind, near gale","good":1},{"id":958,"category":"Additional","description":"gale","good":0},{"id":959,"category":"Additional","description":"severe gale","good":1},{"id":960,"category":"Additional","description":"storm","good":0},{"id":961,"category":"Additional","description":"violent storm","good":0},{"id":962,"category":"Additional","description":"hurricane","good":0}]
    for item in reasonList:
        reason = Reason(item['id'], item['category'], item['description'], item['good'])
        reasons.append(reason)

    return reasons


def sendSMS(result):
	uid = 'thiagolima'
	pwd = 'mashape@4452'
	phone = '5511984049451'
	key = '34ed7617e6085c75e5f4613c6dcfa009'
	headers = [{"name": "X-Mashape-Key", "value": key}, {"name": "Accept", "value": "application/json"}]

	if (result):
		msg = 'FUCK YEAH HARLEY DAVIDSON, MOTHERFUCKER!'
		request = urllib.request.Request("https://site2sms.p.mashape.com/index.php?msg=" + msg + "&phone=" + phone + "&pwd=" + pwd + "&uid=" + uid + "")

		for header in headers:
			request.add_header(header['name'], header['value'])

		response = urllib.request.urlopen(request, cafile=None, capath=None, cadefault=False)
	else:
		msg = 'eh, c3 it is...'
		request = urllib.request.Request("https://site2sms.p.mashape.com/index.php?msg=" + msg + "&phone=" + phone + "&pwd=" + pwd + "&uid=" + uid + "")

		for header in headers:
			request.add_header(header['name'], header['value'])

		response = urllib.request.urlopen(request, cafile=None, capath=None, cadefault=False)


def sendMail(result):
	usr = "thiagocalima@gmail.com"
	pwd = "aqcetfpxlecwoirw"
	sender = "Thiago Lima <thiagocalima@gmail.com>"
	#receivers = ["Bruno Kloss <brunokloss@gmail.com>"]
	receivers = ["Thiago Lima <thiagocalima@gmail.com>"]
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo
	server.starttls()
	server.login(usr, pwd)


	if (result):
		s = "FUCK YEAH HARLEY DAVIDSON, MOTHERFUCKER!"
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (sender, ", ".join(receivers), s, "The today's weapon of choice: " + s)
		try:
			server.sendmail(sender, receivers, message)
		except:
			print ("ERROR: Email not sent!")
	else:
		s = "eh, c3 it is..."
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (sender, ", ".join(receivers), s, "The mainstream veichle for today: " + s)
		try:
			server.sendmail(sender, receivers, message)
		except:
			print ("ERROR: Email not sent!")

	server.close()
		

def main():
    hoje = datetime.now().day

    work = Place("work", Coord("-27.440590", "-48.484183"))
    home = Place("home", Coord("-27.596155", "-48.519980"))

    departureTime = 9
    arrivalTime = 18

    isMotoAllowed = 1

    threshold = 30

    places = [home, work]

    reasons = reasonsBuilder()

    for element in places:

        response = urllib.request.urlopen(urlBuilder(element.coord))

        j = json.loads(response.read().decode("UTF-8"))
        forecast = Forecast(**j)

        for element in forecast.list:

            timestamp = datetime.strptime(element.dt_txt, '%Y-%m-%d %H:%M:%S')

            if (hoje == timestamp.day and timestamp.hour == departureTime):
                for item in element.weather:
                    for reason in reasons:
                        if reason.id == item.id and reason.good == 1:
                            print ("Motorcycle is GOOD in " + forecast.city.name + "! Reason " + str(item.id) + ": " + str(reason.description))
                            isMotoAllowed & 1
                        elif reason.id == item.id and reason.good == 0:
                            print ("Motorcycle is NO good in " + forecast.city.name + "! Reason " + str(item.id) + ": " + str(reason.description))
                            isMotoAllowed & 0

            elif (hoje == timestamp.day and timestamp.hour == arrivalTime):
                for item in element.weather:
                    for reason in reasons:
                        if reason.id == item.id and reason.good == 1:
                            print ("Motorcycle is GOOD in " + forecast.city.name + "! Reason " + str(item.id) + ": " + str(reason.description))
                            isMotoAllowed & 1
                        elif reason.id == item.id and reason.good == 0:
                            print ("Motorcycle is NO good in " + forecast.city.name + "! Reason " + str(item.id) + ": " + str(reason.description))
                            isMotoAllowed & 0

    if (isMotoAllowed):
        #print ("FUCK YEAH HARLEY DAVIDSON, MOTHERFUCKER!")
        #sendSMS(True)
        sendMail(True)
    else:
        #print ("eh, c3 it is...")
        #sendSMS(True)
        sendMail(False)


if __name__ == '__main__':
        sys.exit(main())