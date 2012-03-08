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
from django.utils import simplejson

from django.views.decorators.cache import cache_control

from supportFunc import getLatestData

from decimal import *
import datetime
import re

import employee
import supervisor
import management

messages = {'logout': "You are logged out",
            'login': "You have to log in",
            'wrong': "Wrong username/password"}
accessLevel = {1:'Employee',2:'Supervisor',3:'Management'}
homepage = {1:'/employee',2:'/supervisor',3:'/management'}

'''Support functions - globally used'''
def hello_world(request):    
    now = int(round(time.time() * 1000))
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def authorized(request):
    if request.session.get('auth',False):
        request.session['userType'] =  accessLevel[request.session['accessLevel']]
        return True
    return False

#ajax Page
# How to Return error and cause AJAX call to fail?

#Status - not actual values!
def getUsersStatus(request):    
    if not authorized(request):
        return loginView(request)

    dataOrigin = None
    if request.session['accessLevel'] == 1:
       user = request.session['user']
       return HttpResponse(simplejson.dumps(getLatestData([user])),mimetype="application/javascript") 
    elif request.session['accessLevel'] == 2:
        team = Team.objects.filter(supervisor=request.session['user'])[0]
        return HttpResponse(simplejson.dumps(getLatestData(team.members.all())),mimetype="application/javascript") 
    else: #managment
        searchName = request.POST.get('name',"")
        teamView = request.POST.get('teamView',False)

        if searchName:
            users = Users.objects.filter(name=searchName)

            if teamView:
                users = Team.objects.filter(supervisor=users)[0].members.all() 

            return HttpResponse(simplejson.dumps(getLatestData(users)),mimetype="application/javascript") 
            
       
        return HttpResponse('ERROR') 

#
#Probably won't need
#    
def addToMonitored(request):
    if not authorized(request):
        return loginView(request)
    if request.session['accessLevel'] <= 1:
        return HttpResponse('ERROR')

def removeMonitored(request):
    if not authorized(request):
        return loginView(request)
    if request.session['accessLevel'] <= 1:
        return HttpResponse('ERROR')

def getUsers(request):
    if not authorized(request):
        return loginView(request)
    if request.session['accessLevel'] <= 1:
        return HttpResponse('ERROR')
 
    teamLead = request.POST.get('username','')
    teamLead
    team = Team.objects.filter(supervisor=request.session['user'])[0] 
    retJSON = [] 

    for member in team.members.all():
        retJSON.append({'name':member.name,'profile':'/static/assets/defaultprofile.jpg'})    
    
    return HttpResponse(simplejson.dumps(retJSON),mimetype="application/javascript") 

#Normal Page Views
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
        return redirect(request.session['homepage'])

    if userID and pwd:
        curUser = User.objects.filter(username=userID,password=pwd)

        if len(curUser) == 1:
            curUser = curUser[0]
            request.session['auth'] = True
            request.session['user'] = curUser
            request.session['accessLevel'] = curUser.accessLevel
            request.session['homepage'] = homepage[curUser.accessLevel]

            return redirect(request.session['homepage'])

        else: #should get specific error
	    	c = RequestContext(request, {'auth':False,'errorMessage':messages['wrong']})

    return HttpResponse(t.render(c))

@cache_control(private=True)
def renderDataEmployee(request):
    if not authorized(request):
        return loginView(request)
    return employee.render(request)

@cache_control(private=True)
def renderDataSupervisor(request):
    if not authorized(request):
        return loginView(request)
  
    page = request.GET.get('page','view')

    if page == 'view':
        return supervisor.renderView(request)
    else:
        return supervisor.renderManage(request)

@cache_control(private=True)
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
    User.objects.all().delete()
    SensorData.objects.all().delete()
     
    then = datetime.datetime.now()    
    thenFloat = time.time()*1000000

    abc = User.objects.create(username='e', password='e',accessLevel=1,lastLogin=then,name="ABC",location="US")
    falco = User.objects.create(username='m', password='m',accessLevel=3,lastLogin=then,name="AAA",location="US")
    starfox = User.objects.create(username='s', password='s',accessLevel=2,lastLogin=then,name="BBB",location="US")    

    team1 = Team.objects.create(supervisor=starfox)
    team1.members.add(abc)
    team1.members.add(falco)
    team1.members.add(starfox)

    SensorData.objects.get_or_create(sensorType='T',value='0.4',time=thenFloat, dataNum=1, user=falco) 
    SensorData.objects.get_or_create(sensorType='H',value='50',time=thenFloat, dataNum=1, user=falco) 
    SensorData.objects.get_or_create(sensorType='N',value='10',time=thenFloat, dataNum=1, user=falco)
    SensorData.objects.get_or_create(sensorType='I',value='100',time=thenFloat, dataNum=1, user=falco) 

    SensorData.objects.get_or_create(sensorType='T',value='0.4',time=thenFloat, dataNum=1, user=abc) 
    SensorData.objects.get_or_create(sensorType='H',value='50',time=thenFloat, dataNum=1, user=abc) 
    SensorData.objects.get_or_create(sensorType='N',value='10',time=thenFloat, dataNum=1, user=abc)
    SensorData.objects.get_or_create(sensorType='I',value='100',time=thenFloat, dataNum=1, user=abc)

    SensorData.objects.get_or_create(sensorType='T',value='22.1',time=thenFloat+1, dataNum=2, user=starfox) 
    SensorData.objects.get_or_create(sensorType='H',value='50.0',time=thenFloat+1, dataNum=2, user=starfox) 
    SensorData.objects.get_or_create(sensorType='N',value='10.0',time=thenFloat+1, dataNum=2, user=starfox)
    SensorData.objects.get_or_create(sensorType='I',value='100.0',time=thenFloat+1, dataNum=2, user=starfox) 

    Goal.objects.get_or_create(sensorType='T',value='100.0')
    SafetyConstraint.objects.get_or_create(sensorType='T',maxValue='100',minValue='90')

    html = "<html><body>Added two users with 4 sensorData each</body></html>"
    return HttpResponse(html)    
