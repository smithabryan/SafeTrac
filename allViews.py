from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render_to_response
from chartit import DataPool, Chart

def authorized(request):
    if request.session.get('auth',False):
        return True
    return False
    
def loginView(request):
    userID = request.POST['user']
    pwd = request.POST['pwd']
        
    if userID !="" and pwd !="":
        try:
            curUser = User.objects.filter(username=userID,password=pwd)
            request.session['auth'] = True
            return chartView(request)
        except:
            return render_to_response('base.html',{'auth':False,'errorMessage':'Check username and/or password'})
    else:
        return render_to_response('base.html',{'auth':False,'errorMessage':'You must be logged in.'})
    
def chartView(request):
	#need to get forieign key of user
	#User ID from request OBJ?
    
    if not authorized(request):
        return loginView(request)
        
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

