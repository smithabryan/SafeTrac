'''
Created on Feb 22, 2012

@author: zachgoldstein
'''        
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
            splitData = x.split(" ")
            testString = "22 31 0"
            splitData = testString.split(" ")
            dummyUser = User.objects.get(username='Falco')
            SensorData.objects.get_or_create(sensorType='T',value=splitData[0],time=then, user=dummyUser) 
            SensorData.objects.get_or_create(sensorType='H',value=splitData[1],time=then, user=dummyUser) 
            SensorData.objects.get_or_create(sensorType='N',value=splitData[2],time=then, user=dummyUser)
    #        SensorData.objects.get_or_create(sensorType='I',value=splitData[3],time=then, user=dummyUser) 
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly 
    return x