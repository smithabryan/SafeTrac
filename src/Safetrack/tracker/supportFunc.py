from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team

header = {'logo':'assets/logo.png'}
defaults = {'profilepic':'assets/defaultprofile.jpg'}

def checkStatus(modelObj):
    return {'safety':"Safe",'temp':'12C','humid':'??','noise':'20Db','impact':'0G'}

#def getLatestData(users):
#    res = {}
#    for user in users:
#        safetyConstraints = SafetyConstraint.objects.all()
#        latestTime = SensorData.objects.filter(user=user).order_by('-time')[0]
#
#        latestDataItems = SensorData.objects.filter(time=latestTime.time)
#        temp = latestDataItems.filter(sensorType='T')[0].value
#        noise = latestDataItems.filter(sensorType='N')[0].value
#        humidity = latestDataItems.filter(sensorType='H')[0].value
#        impact = latestDataItems.filter(sensorType='I')[0].value
#
#        # get latest data
#        isSafe = True
#        dangerValues = [];
#        for constraint in safetyConstraints:
#            for dataItem in latestDataItems:
#                if dataItem.sensorType == constraint.sensorType:
#                    if dataItem.value > constraint.maxValue or dataItem.value < constraint.minValue:
#                        isSafe = False
#                        isHigh = False;
#                        sensorName = ""
#                        if dataItem.value > constraint.maxValue:
#                            isHigh = True;
#                        if constraint.sensorType == 'T' : sensorName = "temp"
#                        if constraint.sensorType == 'N' : sensorName = "noise"
#                        if constraint.sensorType == 'I' : sensorName = "impact"
#                        if constraint.sensorType == 'H' : sensorName = "humid"
#
#                        dangerValues.append({
#                                            "cMax":constraint.maxValue,
#                                            "cMin":constraint.minValue,
#                                            "isHigh":isHigh,
#                                            "sensorName":sensorName})
#
#        res[user.name] = {'state':isSafe,'aboveLimits': dangerValues,'temp':temp,'humid':humidity,'noise':noise,'impact':impact}
#
#    return res 

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