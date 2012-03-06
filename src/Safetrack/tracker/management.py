from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from chartit import DataPool, Chart
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from supportFunc import checkStatus

#Management Py.
def renderView(request):
    #groupID = request.session['user'].groupID
    group = User.objects.filter(accessLevel=1)#filtering for members in this supvisor's group; only worker 

    user = User.objects.get(pk=1)
    sensorData = SensorData.objects.filter(sensorType='N')
    latestData = getLatestData(user)

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
    
    #Current Status; check status returns a dictionary
    status = checkStatus(sensorData)
    
    t = loader.get_template('management-view.html')
    c = RequestContext(request, {'auth':True,
                                 'chart1':cht,
                                 'imgsrc':defaults['profilepic'],
                                 'header':header,
                                 'isSafe':latestData[0],
                                 'dangerValues':latestData[1],
                                 'currentValues':latestData[2],
                                 'group':group})

    return HttpResponse(t.render(c))       

def renderManage(request):
    t = loader.get_template('management-manage.html')
    c = RequestContext(request, {'auth':True,
                                 'header':header,
                                })

    return HttpResponse(t.render(c))       
