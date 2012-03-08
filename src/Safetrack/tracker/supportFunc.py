from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from django.http import HttpResponse
from django.utils import simplejson

header = {'logo':'assets/logo.png'}
defaults = {'profilepic':'assets/defaultprofile.jpg'}

def checkStatus(modelObj):
    return {'safety':"Safe",'temp':'12C','humid':'??','noise':'20Db','impact':'0G'}

def getLatestDataX(users):
    safetyConstraints = SafetyConstraint.objects.all()
    res = {}

    for user in users:
        latestDataItem = SensorData.objects.filter(user=user).order_by('-time')[0]
        latestDataItems = SensorData.objects.filter(time=latestDataItem.time)

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
                            if constraint.sensorType == 'T' : sensorName = "temp"
                            if constraint.sensorType == 'N' : sensorName = "noise"
                            if constraint.sensorType == 'I' : sensorName = "impact"
                            if constraint.sensorType == 'H' : sensorName = "humid"
                            dangerValues.append({"dataItem":dataItem.value,"minValue":constraint.minValue,"maxValue":constraint.maxValue,"isHigh":isHigh,"sensorName":sensorName})
        res[user.name] = {'location':user.location,'state':isSafe,'aboveLimits': dangerValues, 'temp':temp,'humid':humidity,'noise':noise,'impact':impact,'time':latestDataItem.time}


    return res

def getLatestData(user):
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
    return {'state':isSafe,'aboveLimits': dangerValues, 'currentValues':{'temp':temp,'humid':humidity,'noise':noise,'impact':impact,'time':latestDataItem.time}}

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
