'''
Created on Feb 21, 2012
@author: zachgoldstein
'''
from django.http import HttpResponse
#from Safetrack.tracker.tasks import SerialReadTask
import datetime
import serial
import time
from django.utils import simplejson

from Safetrack.tracker.supportFunc import *
from Safetrack.tracker import supervisor, employee, management

from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from chartit import DataPool, Chart
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.views.decorators.cache import cache_control

from supportFunc import getLatestDataX, getLatestData
from decimal import *
import datetime
import re

defaults = {'profilepic':'assets/defaultprofile.jpg',
            'logo':'assets/logo.png'}
messages = {'logout': "You are logged out",
            'login': "You have to log in",
            'wrong': "Wrong username/password"}
accessLevel = {1:'Employee',2:'Supervisor',3:'Management'}
homepage = {1:'/employee/',2:'/supervisor/',3:'/management/'}

'''Support functions - globally used'''
def authorized(request):
    if request.session.get('auth',False):
        return True
    return False

##################
#ajax Page
# How to Return error and cause AJAX call to fail?
##################
def getUsersStatus(request):    
    if not authorized(request):
        return loginView(request)

    dataOrigin = None
    if request.session['accessLevel'] == 1:
       user = request.session['user']
       return HttpResponse(simplejson.dumps(getLatestDataX([user])),mimetype="application/javascript") 
    elif request.session['accessLevel'] == 2:
        team = Team.objects.filter(supervisor=request.session['user'])[0]
        return HttpResponse(simplejson.dumps(getLatestDataX(team.members.all())),mimetype="application/javascript") 
    else: #managment
        searchName = request.POST.get('name',"")
        teamView = request.POST.get('teamView',False)

        if searchName:
            users = User.objects.filter(name=searchName)

            if teamView:
                users = Team.objects.filter(supervisor=users)[0].members.all() 

            return HttpResponse(simplejson.dumps(getLatestDataX(users)),mimetype="application/javascript") 
            
        return HttpResponse('ERROR') 

def getGoals(request):
    pass

def setGoals(request):
    pass

def getUsers(request):
    if not authorized(request):
        return loginView(request)
 
    retJSON = [] 

    for user in User.objects.all():
        retJSON.append({'location':user.location,'name':user.name,'profile':'/static/assets/defaultprofile.jpg'})    
    
    return HttpResponse(simplejson.dumps(retJSON),mimetype="application/javascript") 
   
def getMembers(request):
    if not authorized(request):
        return loginView(request)
 
    team = Team.objects.filter(supervisor=request.session['user'])[0] 
    retJSON = [] 

    for member in team.members.all():
        retJSON.append({'location':member.location,'name':member.name,'profile':'/static/assets/defaultprofile.jpg'})    
    
    return HttpResponse(simplejson.dumps(retJSON),mimetype="application/javascript") 

def removeUser(request):
    if not authorized(request):
        return loginView(request)

    team = Team.objects.filter(supervisor=request.session['user'])[0]
    user = User.objects.filter(name=request.GET.get('name'))[0]
    team.members.remove(user)
   
    return HttpResponse('200') 

def addUser(request):
    if not authorized(request):
        return loginView(request)
 
    team = Team.objects.filter(supervisor=request.session['user'])[0] 
    user = User.objects.filter(name=request.GET.get('name'))[0]

    team.members.add(user);
    team.save();

    return HttpResponse('200') 

##################
#Normal Page Views
##################
def logoutView(request):
    request.session.flush()
    
    t = loader.get_template('base.html')
    c = RequestContext(request, {'auth':False,'errorMessage':messages['logout']})

    return HttpResponse(t.render(c))

def loginView(request):
    #if authorized(request):
    #    return redirect(request.session['homepage'])

    userID = request.POST.get('user',False)
    pwd = request.POST.get('pwd',False)
 
    t = loader.get_template('base.html')
    c = RequestContext(request, {'auth':False,'errorMessage':messages['login']})

    if userID and pwd:
        curUser = User.objects.filter(username=userID,password=pwd)

        if curUser.count() == 1:
            curUser = curUser[0]
            request.session['auth'] = True
            request.session['user'] = curUser
            request.session['accessLevel'] = curUser.accessLevel
            request.session['homepage'] = homepage[curUser.accessLevel]
            request.session['userType'] =  accessLevel[request.session['accessLevel']]

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
    

    user = User.objects.get(pk=1)
    sensorData = SensorData.objects.filter(sensorType='N')
    latestData = getLatestData(user)
#    tempSensor = SensorData.objects.filter(sensorType='T', user=user)
#    humidSensor = SensorData.objects.filter(sensorType='H', user=user)
#    noiseSensor = SensorData.objects.filter(sensorType='N', user=user)
#    impactSensor = SensorData.objects.filter(sensorType='I', user=user)
#    SensorData.objects.get_or_create(sensorType='T',value='2',time=datetime.datetime.now(), user=user ) 
   
    '''Getting user data'''
    #Need to fix to grab data
    employeeInfo = {'name':user.username,'title':"Worker"}
    
    '''Creating Charts'''
    dataSeries = \
        DataPool(
            series = 
            [{'options':{'source': sensorData},
            'terms':[
                'value',
                'dataNum']},
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
                  'dataNum': [
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
              {'height': 100,
               'title': {
                   'text': 'Chart'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
    
    '''Current Status; check status returns a dictionary'''
    status = checkStatus(sensorData)
    
    # View code here...
    t = loader.get_template('employee.html')
    c = RequestContext(request,         {'auth':True,
                                         'chart1':cht,
                                         'imgsrc':defaults['profilepic'],
                                         'employeeInfo':employeeInfo,
                                         'header':header,
                                         'isSafe':latestData[0],
                                         'dangerValues':latestData[1],
                                         'currentValues':latestData[2]
                                         })
    return HttpResponse(t.render(c))       
 
def startPolling(request):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    then = datetime.datetime.now()

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
                falco = list(User.objects.filter(username='Falco'))[0]
                roundedDecimalValue = Decimal('%.3f' % float(cleanedData[3]))
                now = str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[0:22]
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

    then = datetime.datetime.now()
    thenString = str(datetime.datetime.strptime(str(then), '%Y-%m-%d %H:%M:%S.%f'))
    thenString = thenString[0:22]
 
    later = then+datetime.timedelta(seconds=1)
    LaterString = str(datetime.datetime.strptime(str(later), '%Y-%m-%d %H:%M:%S.%f'))
    LaterString = LaterString[0:22]
 
    User.objects.all().delete()
    SensorData.objects.all().delete()
        
    added = User.objects.create(username='add', password='e',accessLevel=1,lastLogin=then,email='fa@gl.com',location="US",name="BB")
    abc = User.objects.create(username='e', password='e',accessLevel=1,lastLogin=then,email='falcx@gmail.com',location="US",name="A")
    falco = User.objects.create(username='s', password='s',accessLevel=2,lastLogin=then,email='falcoRox@gmail.com',location="CA",name="AA")
    starfox = User.objects.create(username='m', password='m',accessLevel=3,lastLogin=then,email='starfoxy@gmail.com',location="UK",name="AAA")    
    team1 = Team.objects.create(supervisor=falco)
    team1.members.add(abc)
    team1.members.add(starfox)

    SensorData.objects.get_or_create(sensorType='T',value='0.4',time=thenString, dataNum=1, user=falco) 
    SensorData.objects.get_or_create(sensorType='H',value='50',time=thenString, dataNum=1, user=falco) 
    SensorData.objects.get_or_create(sensorType='N',value='1',time=thenString, dataNum=1, user=falco)
    SensorData.objects.get_or_create(sensorType='I',value='100',time=thenString, dataNum=1, user=falco) 
    SensorData.objects.get_or_create(sensorType='T',value='0.6',time=LaterString, dataNum=1, user=falco) 
    SensorData.objects.get_or_create(sensorType='H',value='60',time=LaterString, dataNum=2, user=falco) 
    SensorData.objects.get_or_create(sensorType='N',value='2',time=LaterString, dataNum=2, user=falco)
    SensorData.objects.get_or_create(sensorType='I',value='110',time=LaterString, dataNum=2, user=falco) 

    SensorData.objects.get_or_create(sensorType='T',value='0.4',time=thenString, dataNum=1, user=abc) 
    SensorData.objects.get_or_create(sensorType='H',value='50',time=thenString, dataNum=1, user=abc) 
    SensorData.objects.get_or_create(sensorType='N',value='1',time=thenString, dataNum=1, user=abc)
    SensorData.objects.get_or_create(sensorType='I',value='100',time=thenString, dataNum=1, user=abc)

    SensorData.objects.get_or_create(sensorType='T',value='22.1',time=thenString, dataNum=2, user=starfox) 
    SensorData.objects.get_or_create(sensorType='H',value='50.0',time=thenString, dataNum=2, user=starfox) 
    SensorData.objects.get_or_create(sensorType='N',value='1',time=thenString, dataNum=2, user=starfox)
    SensorData.objects.get_or_create(sensorType='I',value='100.0',time=thenString, dataNum=2, user=starfox) 

    Goal.objects.get_or_create(sensorType='N',value='2')
    SafetyConstraint.objects.get_or_create(sensorType='N',maxValue='5',minValue='-1')

    html = "<html><body>Added two users with 4 sensorData each</body></html>"
    return HttpResponse(html)    

def getNewChartData(request):
    user = request.session['user']
    latestDataItem = SensorData.objects.filter(user=user)
    latestDataItem = latestDataItem[latestDataItem.count()-1]
    latestDataItems = SensorData.objects.filter(time=latestDataItem.time)
    
    # used in employee.render
    if 'lastNewChartDataTime' not in request.session:
        request.session['lastNewChartDataTime'] = latestDataItem.time
    elif request.session['lastNewChartDataTime'] == latestDataItem.time:
        return HttpResponse([], mimetype='application/javascript')
    else:
        request.session['lastNewChartDataTime'] = latestDataItem.time
    
    dataList = []
    for dataItem in latestDataItems:
        if 'dataViewingType' not in request.session and dataItem.sensorType == 'N':
            dataList.append([dataItem.time,dataItem.value] )    
        elif request.session['dataViewingType'] == "Temp" and dataItem.sensorType == 'T':
            dataList.append([dataItem.time,dataItem.value] )    
        elif request.session['dataViewingType'] == "Noise" and dataItem.sensorType == 'N':
            dataList.append([dataItem.time,dataItem.value] )    
        elif request.session['dataViewingType'] == "Humidity" and dataItem.sensorType == 'H':
            dataList.append([dataItem.time,dataItem.value] )    
        elif request.session['dataViewingType'] == "Impact" and dataItem.sensorType == 'I':
            dataList.append([dataItem.time,dataItem.value] )    
    data = simplejson.dumps(dataList)
    return HttpResponse(data, mimetype='application/javascript')

def testFeedback(request):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    ser.write('@')
    html = "<html><body>Sending an Asterisk to serial port</body></html>"
    return HttpResponse(html)    
