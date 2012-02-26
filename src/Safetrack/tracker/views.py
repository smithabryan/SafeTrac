'''
Created on Feb 21, 2012
@author: zachgoldstein
'''
from django.http import HttpResponse
#from Safetrack.tracker.tasks import SerialReadTask
import datetime
import serial
from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from chartit import DataPool, Chart
from django.shortcuts import render_to_response
from decimal import *
import re

defaults = {'profilepic':'../assets/defaultprofile.jpg',
            'logo':'../assets/logo.png'}
messages = {'logout': "You are logged out",
            'login': "You have to log in",
            'wrong': "Wrong username/password"}
accessLevel = {'1':'Employee','2':'Supervisor','3':'Management'}

header = {'logo':defaults['logo']}

'''Support functions'''
def hello_world(request):    
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def checkStatus(modelObj):
    return {'safety':"Safe",'temp':'12C','humid':'??','noise':'20Db','impact':'0G'}

#Paul's Mod
def authorized(request):
    if request.session.get('auth',False):
        header['accessLevel'] = request.session['accessLevel']
        return True
    return False

'''Views'''
#Paul's Mod    
def logoutView(request):
    request.session['auth'] = False
    request.session['accessLevel'] = 0
    
    return render_to_response('base.html',{'auth':False,'errorMessage': messages['wrong']})
    
def loginView(request):
    userID = "Falco" 
#    request.POST['user']
    pwd = "fuckstarfox"
#    request.POST['pwd']
        
    if userID and pwd:
        curUser = User.objects.filter(username=userID,password=pwd)
        
        if len(curUser) == 1:
            curUser = curUser[0]
            request.session['auth'] = True
            request.session['accessLevel'] = curUser.accessLevel
            return renderDataEmployee(request)
        else: #should get specific error
            return render_to_response('base.html',{'auth':False,'errorMessage':messages['wrong']})
    else:
        return render_to_response('base.html',{'auth':False,'errorMessage':messages['login']})

def login(request):
    then = datetime.datetime.now()
    dummyUser = User(username='Falco', password='fuckstarfox',accessLevel=3,lastLogin=then,email='falcoRox@gmail.com')
    dummyUser.save()
    request.session['userLoggedIn'] = dummyUser    
    html = "<html><body>Added user</body></html>"
    return HttpResponse(html)

def renderDataEmployee(request):
#Paul's Mod
#    if not authorized(request):
#        return loginView(request)
        
#    user = User.objects.get(username='Falco')
    #need to get forieign key of user
    #User ID from request OBJ?
#
    user = User.objects.get(pk=1)
    sensorData = SensorData.objects.all()
#    tempSensor = SensorData.objects.filter(sensorType='T', user=user)
#    humidSensor = SensorData.objects.filter(sensorType='H', user=user)
#    noiseSensor = SensorData.objects.filter(sensorType='N', user=user)
#    impactSensor = SensorData.objects.filter(sensorType='I', user=user)
#    SensorData.objects.get_or_create(sensorType='T',value='2',time=datetime.datetime.now(), user=user ) 
    
    '''Getting user data'''
    #employeeInfo = {'name':user.name,'title':user.title}
    employeeInfo = {'name':"Mr. ABC", 'title': "Hello World"}
    
    '''Creating Charts'''
    dataSeries = \
        DataPool(
            series = 
            [{'options':{'source': sensorData},
            'terms':[
                'value',
                'value']},
#            '''
#            {'options':{'source': SensorDataInteger.objects.all()},
#            'terms':[
#                'value',
#                'value']}
#            '''    
            ]);
    cht = Chart(
            datasource = dataSeries,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'value': [
                    'value']
                  }},
#              '''
#               {'options':{
#               'type': 'line',
#              'stacking': False},
#            'terms':{
#              'value': [
#                'value']
#              }}
#              '''
                ],
            chart_options =
              {'title': {
                   'text': 'Chart'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
    
    '''Current Status; check status returns a dictionary'''
    status = checkStatus(sensorData)
    
    #might have to check auth
    return render_to_response('employee.html',{'auth':True,'chart1':cht,'imgsrc':defaults['profilepic'],'employeeInfo':employeeInfo,'header':header})   
    
def startPolling(request):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    then = datetime.datetime.now()
    while ( (datetime.datetime.now() - then) < datetime.timedelta(seconds=30)):
        x = ser.readline(30)
        print x
        try:
            cleanedData = []
            for dataString in x.split(" "):
                if dataString != '' or dataString != '\n':
                    splitItem = re.sub(r'[^\w.]', '', dataString)
                    cleanedData.append(splitItem)
            if len(cleanedData) == 4:
                dummyUser = User.objects.get(pk=1)
                roundedDecimalValue = Decimal('%.3f' % float(cleanedData[3]))
                SensorData.objects.get_or_create(sensorType='T',value=cleanedData[0],time=then, user=dummyUser) 
                SensorData.objects.get_or_create(sensorType='H',value=cleanedData[1],time=then, user=dummyUser) 
                SensorData.objects.get_or_create(sensorType='N',value=cleanedData[2],time=then, user=dummyUser)
                SensorData.objects.get_or_create(sensorType='I',value=roundedDecimalValue,time=then, user=dummyUser) 
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

    Goal.objects.get_or_create(sensorType='T',value='100.0')
    SafetyConstraint.objects.get_or_create(sensorType='T',maxValue='45.0',minValue='-10.0')

    html = "<html><body>Added two users with 4 sensorData each</body></html>"
    return HttpResponse(html)    
