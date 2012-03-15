from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from chartit import DataPool, Chart
from django.http import HttpResponse
from django.template import RequestContext, loader

from Safetrack.tracker.supportFunc import *

#Employee?
def render(request):
    user = request.session['user']
    request.session['dataViewingType'] = "Noise"
    sensorData = SensorData.objects.filter(sensorType='N', user=user)[0:10]
    latestData = getLatestData(user)
    request.session['lastNewChartDataTime'] = latestData['currentValues']['time']
#    tempSensor = SensorData.objects.filter(sensorType='T', user=user)
#    humidSensor = SensorData.objects.filter(sensorType='H', user=user)
#    noiseSensor = SensorData.objects.filter(sensorType='N', user=user)
#    impactSensor = SensorData.objects.filter(sensorType='I', user=user)
#    SensorData.objects.get_or_create(sensorType='T',value='2',time=datetime.datetime.now(), user=user ) 
   
    '''Getting user data'''
    #Need to fix to grab data
    employeeInfo = {'Name':user.name,'Title':"Worker",'Location': user.location}
    
    '''Creating Charts'''
    dataSeries = DataPool(
            series = 
            [{'options':{'source': sensorData},
            'terms':[
                'value',
                'time']},
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
                  }},
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
   
    header['userType'] = request.session['userType']
 
    # View code here...
    t = loader.get_template('employee.html')
    c = RequestContext(request,         {'auth':True,
                                         'chart1':cht,
                                         'imgsrc':defaults['profilepic'],
                                         'employeeInfo':employeeInfo,
                                         'header':header,
                                         'isSafe':latestData['state'],
                                         'dangerValues':latestData['aboveLimits'],
                                         'currentValues':latestData['currentValues']
                                         })
    return HttpResponse(t.render(c))       
