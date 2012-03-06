'''
Created on Feb 21, 2012
@author: zachgoldstein
'''
from django.http import HttpResponse
#from Safetrack.tracker.tasks import SerialReadTask
import datetime
import serial
import time

from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from chartit import DataPool, Chart
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.context_processors import csrf

from decimal import *
import datetime
import re

import employee
import supervisor
import management
defaults = {'profilepic':'assets/defaultprofile.jpg',
            'logo':'assets/logo.png'}
messages = {'logout': "You are logged out",
            'login': "You have to log in",
            'wrong': "Wrong username/password"}
accessLevel = {1:'Employee',2:'Supervisor',3:'Management'}
homepage = {1:'/employee',2:'/supervisor',3:'/management'}
header = {'logo':defaults['logo'],'homepage':''}

'''Support functions - global used'''
def hello_world(request):    
    now = int(round(time.time() * 1000))
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def authorized(request):
    if request.session.get('auth',False):
        header['userType'] = accessLevel[request.session['accessLevel']]
        return True
    return False

#Views
def logoutView(request):
    request.session.flush()
    
    t = loader.get_template('base.html')
    c = RequestContext(request, {'auth':False,'errorMessage':messages['logout']})

    return HttpResponse(t.render(c))

def loginView(request):
    userID = request.POST.get('user',False)
    pwd = request.POST.get('pwd',False)

    t = loader.get_template('base.html')
    c = RequestContext(request, {'auth':False,'errorMessage':messages['login']})

    if authorized(request):
        return redirect(header['homepage'])

    if userID and pwd:
        curUser = User.objects.filter(username=userID,password=pwd)

        if len(curUser) == 1:
            curUser = curUser[0]
            request.session['auth'] = True
            request.session['user'] = curUser
            request.session['accessLevel'] = curUser.accessLevel

            header['homepage'] = homepage[curUser.accessLevel]

            return redirect(header['homepage'])

        else: #should get specific error
	    	c = RequestContext(request, {'auth':False,'errorMessage':messages['wrong']})

    return HttpResponse(t.render(c))

def getLatestData(user):
    safetyConstraints = SafetyConstraint.objects.all()
    latestDataItem = SensorData.objects.filter(user=user).order_by('-time')[0]
    latestDataItems = SensorData.objects.filter(time=latestDataItem.time)
    temp = latestDataItems.filter(sensorType='T')[0].value
    noise = latestDataItems.filter(sensorType='N')[0].value
    humidity = latestDataItems.filter(sensorType='H')[0].value
    impact = latestDataItems.filter(sensorType='I')[0].value
    # get latest data
    
    isSafe = True
    dangerValues = [];
    for constraint in safetyConstraints:
        for dataItem in latestDataItems:
            if dataItem.sensorType == constraint.sensorType:
                if dataItem.value > constraint.maxValue or dataItem.value < constraint.minValue:
                    isSafe = False
                    isHigh = False;
                    sensorName = ""
                    if dataItem.value > constraint.maxValue:
                        isHigh = True;
                    if constraint.sensorType == 'T' : sensorName = "Temperature"
                    if constraint.sensorType == 'N' : sensorName = "Noise"
                    if constraint.sensorType == 'I' : sensorName = "Impact"
                    if constraint.sensorType == 'H' : sensorName = "Humidity"
                    dangerValues.append({"dataItem":dataItem,"constraint":constraint,"isHigh":isHigh,"sensorName":sensorName})
    return [isSafe, dangerValues, {'temp':temp,'humid':humidity,'noise':noise,'impact':impact}]

def renderDataEmployee(request):
    if not authorized(request):
        return loginView(request)
    return employee.render(request)
 
def renderDataSupervisor(request):
    if not authorized(request):
        return loginView(request)
  
    page = request.GET.get('page','view')

    if page == 'view':
        return supervisor.renderView(request)
    else:
        return supervisor.renderManage(request)

def renderDataManagement(request):
    if not authorized(request):
        return loginView(request)
  
    page = request.GET.get('page','view')

    if page == 'view':
        return management.renderView(request)
    else:
        return management.renderManage(request)
    
def startPolling(request):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    then = datetime.datetime.now()
    now = int(round(time.time() * 1000))
    numDataTaken = 0
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
#                dummyUser = User.objects.get(pk=1)
                falco = User.objects.create(username='Falco', password='starfoxisawimp',accessLevel=3,lastLogin=then,email='falcoRox@gmail.com')
                roundedDecimalValue = Decimal('%.3f' % float(cleanedData[3]))
                print "noise,time is ("+repr(cleanedData[2])+","+repr(now)+")"
                SensorData.objects.get_or_create(sensorType='T',value=cleanedData[0],time=now, dataNum=numDataTaken, user=falco) 
                SensorData.objects.get_or_create(sensorType='H',value=cleanedData[1],time=now, dataNum=numDataTaken, user=falco) 
                SensorData.objects.get_or_create(sensorType='N',value=cleanedData[2],time=now, dataNum=numDataTaken, user=falco)
                SensorData.objects.get_or_create(sensorType='I',value=roundedDecimalValue,time=now, dataNum=numDataTaken, user=falco) 
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
    thenFloat = time.time()*1000000
    #abc = User.objects.create(username='abc', password='abc',accessLevel=1,lastLogin=then,email='falcx@gmail.com')
    #falco = User.objects.create(username='Falco', password='starfoxisawimp',accessLevel=3,lastLogin=then,email='falcoRox@gmail.com')
   #starfox = User.objects.create(username='', password='falcocantfly',accessLevel=3,lastLogin=then,email='starfoxy@gmail.com')    
    starfox = User.objects.create(username='ppp', password='ppp',accessLevel=2,lastLogin=then,email='starfoxy@gmail.com')    

#    SensorData.objects.get_or_create(sensorType='T',value='0.4',time=thenFloat, dataNum=1, user=falco) 
#    SensorData.objects.get_or_create(sensorType='H',value='50',time=thenFloat, dataNum=1, user=falco) 
#    SensorData.objects.get_or_create(sensorType='N',value='10',time=thenFloat, dataNum=1, user=falco)
#    SensorData.objects.get_or_create(sensorType='I',value='100',time=thenFloat, dataNum=1, user=falco) 

#    SensorData.objects.get_or_create(sensorType='T',value='0.4',time=thenFloat, dataNum=1, user=abc) 
#    SensorData.objects.get_or_create(sensorType='H',value='50',time=thenFloat, dataNum=1, user=abc) 
#    SensorData.objects.get_or_create(sensorType='N',value='10',time=thenFloat, dataNum=1, user=abc)
#    SensorData.objects.get_or_create(sensorType='I',value='100',time=thenFloat, dataNum=1, user=abc)

    SensorData.objects.get_or_create(sensorType='T',value='22.1',time=thenFloat+1, dataNum=2, user=starfox) 
    SensorData.objects.get_or_create(sensorType='H',value='50.0',time=thenFloat+1, dataNum=2, user=starfox) 
    SensorData.objects.get_or_create(sensorType='N',value='10.0',time=thenFloat+1, dataNum=2, user=starfox)
    SensorData.objects.get_or_create(sensorType='I',value='100.0',time=thenFloat+1, dataNum=2, user=starfox) 

    Goal.objects.get_or_create(sensorType='T',value='100.0')
    SafetyConstraint.objects.get_or_create(sensorType='T',maxValue='100',minValue='90')

    html = "<html><body>Added two users with 4 sensorData each</body></html>"
    return HttpResponse(html)    
