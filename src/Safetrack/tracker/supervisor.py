from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from chartit import DataPool, Chart
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from Safetrack.tracker.supportFunc import *

#Supervisor Py.
def renderView(request):
    #assuming only managing 1 team
    team = Team.objects.filter(supervisor=request.session['user'])[0]
  
    sensorData = SensorData.objects.filter(sensorType='N')[0:10]
    latestData = getLatestData(team.members.all())

    #groupID = request.session['user'].groupID
    group = User.objects.filter(accessLevel=1)#filtering for members in this supvisor's group; only worker 

    dataSeries = \
        DataPool(
            series = 
            [{'options':{'source': sensorData},
            'terms':[
                'value',
                'dataNum']},
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
                ],
            chart_options =
              {'height': 100,
               'title': {
                   'text': 'Chart'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
    
    #status = checkStatus(sensorData)
    header['userType'] = request.session['userType']

    t = loader.get_template('supervisor-view.html')
    c = RequestContext(request, {'auth':True,
                                 'chart1':cht,
                                 'imgsrc':defaults['profilepic'],
                                 'header':header,
                                 'workerState':latestData,
                                 'group':group})

    return HttpResponse(t.render(c))       

def renderManage(request):
    t = loader.get_template('supervisor-manage.html')
    header['userType'] = request.session['userType']

    c = RequestContext(request, {'auth':True,
                                 'header':header,
                                })

    return HttpResponse(t.render(c))    
