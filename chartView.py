from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render_to_response
from chartit import DataPool, Chart

def basic(request):
	#need to get forieign key of user
	#User ID from request OBJ?

	tempSensor = Sensor.objects.filter(sensorType='T', user=userID)
	humidSensor = Sensor.objects.filter(sensorType='H', user=userID)
	noiseSensor = Sensor.objects.filter(sensorType='N', user=userID)
	impactSensor = Sensor.objects.filter(sensorType='I', user=userID)

	#Create DataPool
	dataSeries = \
		DataPool(
			series = 
			[{'options':{'source': tempSensor},
			'terms':[
				'time',
				'y']}
			]);
	cht = Chart(
            datasource = dataSeries,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'time': [
                    'y']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Chart'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
	
	return render_to_response('employee.html',{'chart1':cht})
