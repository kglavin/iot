
# sample data collection app running on an IOT gateway. 
# this app will receive data metrics from the iot things, 
# does not run on micropython -- is used on host that micropthon hosts 
# connects to.

import sys

from flask import Flask, redirect, url_for, request, Response
app = Flask(__name__)

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route('/')
def success():
   return 'This is the iot data collector\r\n'

@app.route('/data/<machineid>')
def show_machine_config(machineid):
    return 'Machine %s' % machineid

@app.route('/data',methods = ['POST', 'GET'])
def data():
   if request.method == 'POST':
   		#user = request.form['nm']
   		data = request.get_data()
   		#print(data, file=sys.stdout)
   		return  Response('success\r\n','text/text')
   else:
   	return 'There is not data here for you to get\r\n'

if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	app.run(debug = True, host='0.0.0.0', port=2000)