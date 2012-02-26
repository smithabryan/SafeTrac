'''
Created on Feb 22, 2012

@author: zachgoldstein
'''        
from celery.decorators import task
from Safetrack.tracker.models import SensorData
from Safetrack.tracker.models import User
import serial
import datetime
from decimal import *
import re

@task
def SerialReadTask(username, **kwargs):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    then = datetime.datetime.now()
    while ( (datetime.datetime.now() - then) < datetime.timedelta(seconds=30)):
        x = ser.readline(30)
        print x
        try:
            cleanedData = []
            for dataString in x.split(" "):
                if dataString != '' or dataString != '\n':
                    splitItem = re.sub(r'[^\w.]', '', dataString)
                    cleanedData.append(splitItem)
            if len(cleanedData) == 4:
                dummyUser = User.objects.get(pk=1)
                roundedDecimalValue = Decimal('%.3f' % float(cleanedData[3]))
                SensorData.objects.get_or_create(sensorType='T',value=cleanedData[0],time=then, user=dummyUser) 
                SensorData.objects.get_or_create(sensorType='H',value=cleanedData[1],time=then, user=dummyUser) 
                SensorData.objects.get_or_create(sensorType='N',value=cleanedData[2],time=then, user=dummyUser)
                SensorData.objects.get_or_create(sensorType='I',value=roundedDecimalValue,time=then, user=dummyUser) 
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
    return x