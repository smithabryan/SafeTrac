from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import simplejson
import serial
from django.db.models.query import QuerySet
import datetime

header = {'logo':'assets/logo.png'}
defaults = {'profilepic':'assets/defaultprofile.jpg'}

def checkStatus(modelObj):
    return {'safety':"Safe",'temp':'12C','humid':'??','noise':'20Db','impact':'0G'}

def getLatestDataX(users):
    
    safetyConstraints = SafetyConstraint.objects.all()
    res = {}

    for user in users:
        latestDataItem = SensorData.objects.filter(user=user).order_by('-time')[0]
        UserModelObj = User.objects.get(username=user.username)
        latestDataItems = UserModelObj.sensordata_set.all().filter(time=latestDataItem.time)
#        latestDataItems = SensorData.objects.filter(time=latestDataItem.time)

        temps = latestDataItems.filter(sensorType='T')
        noises = latestDataItems.filter(sensorType='N')
        humidities = latestDataItems.filter(sensorType='H')
        impacts = latestDataItems.filter(sensorType='I')
        temp,noise,humidity,impact = -1,-1,-1,-1

        if temps.count() > 0:
            temp = temps[0].value
        if noises.count() > 0:
            noise = noises[0].value
        if humidities.count() > 0:
            humidity = humidities[0].value
        if impacts.count() > 0:
            impact = impacts[0].value

        if latestDataItems.count() > 0:
            # get latest data
            isSafe = True
            dangerValues = [];
            for constraint in safetyConstraints:
                print "constraint type is"+constraint.sensorType
                for dataItem in latestDataItems:
                    print "data type is"+dataItem.sensorType
#                    dataItem = latestDataItem
                    if dataItem.sensorType == constraint.sensorType:
                        if dataItem.value > constraint.maxValue: # or dataItem.value < constraint.minValue:
                            isSafe = False
                            isHigh = False;
                            sensorName = ""
    
                            if dataItem.value > constraint.maxValue:
                                isHigh = True;
                            if constraint.sensorType == 'T' : sensorName = "temp"
                            if constraint.sensorType == 'N' : sensorName = "noise"
                            if constraint.sensorType == 'I' : sensorName = "impact"
                            if constraint.sensorType == 'H' : sensorName = "humid"
                            dangerValues.append({"dataItem":dataItem.value,"minValue":constraint.minValue,"maxValue":constraint.maxValue,"isHigh":isHigh,"sensorName":sensorName})
        res[user.username] = {'name':user.name,'location':user.location,'state':isSafe,'aboveLimits': dangerValues, 'temp':temp,'humid':humidity,'noise':noise,'impact':impact,'time':latestDataItem.time}

    return res

def getLatestData(user):
    if isinstance(user, QuerySet):
        if user.count() == 0:
            return {}
    safetyConstraints = SafetyConstraint.objects.all()
    latestDataItem = SensorData.objects.filter(user=user).order_by('-time')[0]
    latestDataItems = SensorData.objects.filter(time=latestDataItem.time)
    # get latest data
    temps = latestDataItems.filter(sensorType='T')
    noises = latestDataItems.filter(sensorType='N')
    humidities = latestDataItems.filter(sensorType='H')
    impacts = latestDataItems.filter(sensorType='I')
    temp,noise,humidity,impact = -1,-1,-1,-1
    if temps.count() > 0:
        temp = temps[0].value
    if noises.count() > 0:
        noise = noises[0].value
    if humidities.count() > 0:
        humidity = humidities[0].value
    if impacts.count() > 0:
        impact = impacts[0].value

    if latestDataItems.count() > 0:
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

    returnData = {'state':isSafe,'aboveLimits': dangerValues, 'currentValues':{'temp':temp,'humid':humidity,'noise':noise,'impact':impact,'time':latestDataItem.time}}
    serialSafetyFeedback(returnData)    
    return returnData

def getTemperatureData(request):
    request.session['dataViewingType'] = "Temp"
    user = request.session['user']
    sensorDataList = SensorData.objects.filter(sensorType='T', user=user)[0:10]
    returnListValues = []
    returnListTimes = []
    for sensorData in sensorDataList:
        returnListValues.append(sensorData.value)
        returnListTimes.append(sensorData.time)
    data = simplejson.dumps([returnListValues,returnListTimes])
    return HttpResponse(data, mimetype='application/javascript')

#TODO: factor out a method here to reduce overlap 
def getNoiseData(request):
    request.session['dataViewingType'] = "Noise"
    user = request.session['user']
    sensorDataList = SensorData.objects.filter(sensorType='N', user=user)[0:10]
    returnListValues = []
    returnListTimes = []
    for sensorData in sensorDataList:
        returnListValues.append(sensorData.value)
        returnListTimes.append(sensorData.time)
    data = simplejson.dumps([returnListValues,returnListTimes])
    return HttpResponse(data, mimetype='application/javascript')
def getHumidityData(request):
    request.session['dataViewingType'] = "Humidity"
    user = request.session['user']
    sensorDataList = SensorData.objects.filter(sensorType='H', user=user)[0:10]
    returnListValues = []
    returnListTimes = []
    for sensorData in sensorDataList:
        returnListValues.append(sensorData.value)
        returnListTimes.append(sensorData.time)
    data = simplejson.dumps([returnListValues,returnListTimes])
    return HttpResponse(data, mimetype='application/javascript')
def getImpactData(request):
    request.session['dataViewingType'] = "Impact"
    user = request.session['user']
    sensorDataList = SensorData.objects.filter(sensorType='I', user=user)[0:10]
    returnListValues = []
    returnListTimes = []
    for sensorData in sensorDataList:
        returnListValues.append(sensorData.value)
        returnListTimes.append(sensorData.time)
    data = simplejson.dumps([returnListValues,returnListTimes])
    return HttpResponse(data, mimetype='application/javascript')

def serialSafetyFeedbackAjax(request):
    user = request.session['user']
    latestData = getLatestData(user)
    serialSafetyFeedback(latestData)
    return HttpResponse([], mimetype='application/javascript')

def serialSafetyFeedback(latestData):
    try:
        ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
        user = User.objects.filter(username='e')
        latestDataItem = SensorData.objects.filter(user=user, sensorType='N').order_by('-time')[0]
        noiseGoal = SafetyConstraint.objects.filter(sensorType='N')[0]
        if latestDataItem.value > noiseGoal.gmaxValue:
            ser.write('$@') 
        else:
            ser.write('$*')
    except: 
        print "Serial not connected"    
        
def serialSafetyRefresh(request):
    t = loader.get_template('safety.html')
    user = request.session['user']
    latestData = getLatestData(user)
    c = RequestContext(request,         {'isSafe':latestData['state'],
                                         'dangerValues':latestData['aboveLimits'],
                                         'currentValues':latestData['currentValues']
                                         })
    response = HttpResponse(t.render(c))
    return response

def getGoalData(request):
    #We're just going to return an array with ten of the goal items
    #will take the first goal if  multiple goals are of a single sensorType 
    type = request.session['dataViewingType']
    sensorType = ""
    if type == "Temperature":
        sensorType = "T"
    elif type == "Noise":
        sensorType = "N"
    elif type == "Humidity":
        sensorType = "H"
    elif type == "Impact":
        sensorType = "I"
    goal = Goal.objects.filter(sensorType=sensorType)
    if goal.count() > 0:
        goal = goal[0]
    else:
        data = simplejson.dumps([])
        return HttpResponse(data, mimetype='application/javascript')
    datalist = []
    if goal:
        for i in xrange(0,10,1):
            datalist.append(goal.value)
    data = simplejson.dumps(datalist)
    return HttpResponse(data, mimetype='application/javascript')

#Note this approach is brute force, and very inefficient
def getAllData(request):
    users = User.objects.all()
    goals = SafetyConstraint.objects.all()
    dataDict = {}
    dataDict['times'] = []
    
    for user in users:
        dataDict[user.username] = {}
        userSensorData = SensorData.objects.filter(user=user).order_by('-time')
        for sensorData in userSensorData:
            if sensorData.time not in dataDict['times']:
                dataDict['times'].append(sensorData.time)
            if sensorData.sensorType in dataDict[user.username]:
                dataDict[user.username][sensorData.sensorType].append(sensorData.value)
            else :
                dataDict[user.username][sensorData.sensorType] = []
                dataDict[user.username][sensorData.sensorType].append(sensorData.value)
    
    dataDict['goals'] = {}
    for goal in goals:
        if goal.sensorType not in dataDict['goals']:
            dataDict['goals'][goal.sensorType] = [];
            dataDict['goals'][goal.sensorType].append(goal.gmaxValue)
    data = simplejson.dumps(dataDict)
    return HttpResponse(data, mimetype='application/javascript') 

def checkIfConnected(request):
    lastDataItem = SensorData.objects.order_by('-created')[0]
    lastTime = lastDataItem.created
    timeSinceData = datetime.datetime.now() - lastTime
    if (timeSinceData > datetime.timedelta(seconds=15)):
        data = simplejson.dumps(True)
        return HttpResponse(data, mimetype='application/javascript') 
    else :
        data = simplejson.dumps(False)
        return HttpResponse(data, mimetype='application/javascript')
