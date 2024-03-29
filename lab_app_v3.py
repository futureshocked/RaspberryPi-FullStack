'''
FILE NAME
lab_app.py
Version 3

1. WHAT IT DOES
This version contains allows the selection of records from the database by defining a date range in the request URL.
 
2. REQUIRES
* Any Raspberry Pi

3. ORIGINAL WORK
Raspberry Full Stack 2015, Peter Dalmaris

4. HARDWARE
* Any Raspberry Pi
* DHT11 or 22
* 10KOhm resistor
* Breadboard
* Wires

5. SOFTWARE
Command line terminal
Simple text editor
Libraries:
from flask import Flask, request, render_template, sqlite3

6. WARNING!
None

7. CREATED 

8. TYPICAL OUTPUT
A simple web page served by this flask application in the user's browser.
The page contains the current temperature and humidity.
A second page that displays historical environment data from the SQLite3 database.
The historical records can be selected by specifying a date range in the request URL.

 // 9. COMMENTS
--
 // 10. END
'''
from flask import Flask, request, render_template
import time
import datetime

app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/lab_temp")
def lab_temp():
	import sys
	import Adafruit_DHT
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	if humidity is not None and temperature is not None:
		return render_template("lab_temp.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")

@app.route("/lab_env_db", methods=['GET']) 
def lab_env_db():
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
	import sqlite3
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs=conn.cursor()
	# curs.execute("SELECT * FROM temperatures")
	# temperatures = curs.fetchall()
	# curs.execute("SELECT * FROM humidities")
	# humidities = curs.fetchall()
	# conn.close()
	curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	temperatures 	= curs.fetchall()
	curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	humidities 		= curs.fetchall()
	conn.close()
	return render_template("lab_env_db.html",temp=temperatures,hum=humidities)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
