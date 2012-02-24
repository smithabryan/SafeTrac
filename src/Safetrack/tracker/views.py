'''
Created on Feb 21, 2012

@author: zachgoldstein
'''
from django.http import HttpResponse
#from Safetrack.tracker.tasks import SerialReadTask
import datetime
import serial
from Safetrack.tracker.models import SensorData
from Safetrack.tracker.models import User
from chartit import DataPool, Chart
from django.shortcuts import render_to_response

def hello_world(request):    
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def login(request):
    then = datetime.datetime.now()
    dummyUser = User(username='Falco', password='fuckstarfox',accessLevel=3,lastLogin=then,email='falcoRox@gmail.com')
    dummyUser.save()
    request.session['userLoggedIn'] = dummyUser    
    html = "<html><body>Added user</body></html>"
    return HttpResponse(html)

def renderDataEmployee(request):
    #need to get forieign key of user
    #User ID from request OBJ?
#
#    user = User.objects.get(username='Falco')
#    tempSensor = SensorData.objects.filter(sensorType='T', user=user)
#    humidSensor = SensorData.objects.filter(sensorType='H', user=user)
#    noiseSensor = SensorData.objects.filter(sensorType='N', user=user)
#    impactSensor = SensorData.objects.filter(sensorType='I', user=user)

    #Create DataPool
    dataSeries = \
        DataPool(
            series = 
            [{'options':{'source': SensorData.objects.all()},
            'terms':[
                'time',
                'value']}
            ]);
    cht = Chart(
            datasource = dataSeries,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'time': [
                    'value']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Chart'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
    
    return render_to_response('employee.html',{'chart1':cht})    
    

def startPolling(request):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    then = datetime.datetime.now()
    while ( (datetime.datetime.now() - then) < datetime.timedelta(seconds=30)):
        x = ser.readline(30)
        print x
        try:
            splitData = x.split(" ")
            testString = "22 31 0"
            splitData = testString.split(" ")
            dummyUser = User.objects.get(username='Falco')
            SensorData.objects.get_or_create(sensorType='T',value=splitData[0],time=then, user=dummyUser) 
            SensorData.objects.get_or_create(sensorType='H',value=splitData[1],time=then, user=dummyUser) 
            SensorData.objects.get_or_create(sensorType='N',value=splitData[2],time=then, user=dummyUser)
    #        SensorData.objects.get_or_create(sensorType='I',value=splitData[3],time=then, user=dummyUser) 
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
    html = "<html><body>Starting to poll</body></html>"
    return HttpResponse(html)

def testSendFromServer(request):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    ser.write(2)
    html = "<html><body>Wrote 2 to serial</body></html>"
    return HttpResponse(html)    

def addDummyDataToDb(request):
    then = datetime.datetime.now()    
    falco = User.objects.create(username='Falco', password='starfoxisawimp',accessLevel=3,lastLogin=then,email='falcoRox@gmail.com')
    starfox = User.objects.create(username='Starfox', password='falcocantfly',accessLevel=3,lastLogin=then,email='starfoxy@gmail.com')    

    SensorData.objects.get_or_create(sensorType='T',value='0.0',time=then, user=falco) 
    SensorData.objects.get_or_create(sensorType='H',value='50',time=then, user=falco) 
    SensorData.objects.get_or_create(sensorType='N',value='10',time=then, user=falco)
    SensorData.objects.get_or_create(sensorType='I',value='100',time=then, user=falco) 

    SensorData.objects.get_or_create(sensorType='T',value='22.1',time=then, user=starfox) 
    SensorData.objects.get_or_create(sensorType='H',value='50.0',time=then, user=starfox) 
    SensorData.objects.get_or_create(sensorType='N',value='10.0',time=then, user=starfox)
    SensorData.objects.get_or_create(sensorType='I',value='100.0',time=then, user=starfox) 

    html = "<html><body>Added two users with 4 sensorData each</body></html>"
    return HttpResponse(html)    
    