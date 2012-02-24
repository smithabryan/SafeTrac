'''
Created on Feb 22, 2012

@author: zachgoldstein
'''        
from celery.app.task import BaseTask
from celery.registry import tasks
from celery.decorators import task
from Safetrack.tracker.models import SensorData
from Safetrack.tracker.models import User
import serial
import datetime

@task
def SerialReadTask(username, **kwargs):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    then = datetime.datetime.now()
    while ( (datetime.datetime.now() - then) < datetime.timedelta(seconds=30)):
        x = ser.readline(30)
        print x
        try:        
            testString = "22 31 0"
            splitData = testString.split(" ")
            for str in splitData:
                if( "C" in str):
                    print str.strip('C')
                elif( "db" in str ):
                    print str.strip('db')
                else:
                    print str.strip('%')
            dummyUser = User.objects.get(username=username)
            sensorData = SensorData(sensorType='T',value='0.0',time=then, user=dummyUser)
            sensorData.save()
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly   
    return x