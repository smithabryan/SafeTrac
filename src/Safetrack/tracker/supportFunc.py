from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team

header = {'logo':'assets/logo.png'}
defaults = {'profilepic':'assets/defaultprofile.jpg'}

def checkStatus(modelObj):
    return {'safety':"Safe",'temp':'12C','humid':'??','noise':'20Db','impact':'0G'}

def getLatestData(users):
    res = {}
    for user in users:
        safetyConstraints = SafetyConstraint.objects.all()
        latestTime = SensorData.objects.filter(user=user).order_by('-time')[0]

        latestDataItems = SensorData.objects.filter(time=latestTime.time)
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
        res[user.username] = {'state':isSate,'dangerValue': dangerValues,'temp':temp,'humid':humidity,'noise':noise,'impact':impact}
    return HttpResponse(simplejson.dumps(res),mimetype="application/javascript") 
