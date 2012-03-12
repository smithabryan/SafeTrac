from Safetrack.tracker.models import SensorData, User, Goal, SafetyConstraint, Team
from chartit import DataPool, Chart
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from Safetrack.tracker.supportFunc import *

#Management Py.
def renderView(request):
    t = loader.get_template('management-view.html')
    c = RequestContext(request, {'auth':True,
                                 'header':header,
                                })


    return HttpResponse(t.render(c))       

def renderManage(request):
    t = loader.get_template('management-manage.html')
    c = RequestContext(request, {'auth':True,
                                 'header':header,
                                })

    return HttpResponse(t.render(c))       
