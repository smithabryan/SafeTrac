'''
Created on Feb 22, 2012

@author: zachgoldstein
'''        
from celery.decorators import task, periodic_task
from Safetrack.tracker.models import SensorData
from Safetrack.tracker.models import User
import serial
import datetime
from decimal import *
import re
from celery.task import task, PeriodicTask
from celery.schedules import crontab
from datetime import timedelta
import random

@task  
def SerialReadTask(username, time, **kwargs):
    ser = serial.Serial('/dev/tty.usbmodemfa131',9600, timeout=1)
    then = datetime.datetime.now()

    numDataTaken = 0
    while ( (datetime.datetime.now() - then) < datetime.timedelta(seconds=30)):
        try:
            x = ser.read(30)
            print x
            cleanedData = []
            for dataString in x.split(" "):
                if dataString != '' or dataString != '\n':
                    splitItem = re.sub(r'[^\w.]', '', dataString)
                    cleanedData.append(splitItem)
#            extra clean, stuff sometimes sneaks in?
            for dataString in cleanedData:
                if dataString == '':
                    cleanedData.remove(dataString)                    
            if len(cleanedData) == 4:
#                dummyUser = User.objects.get(pk=1)
                falco = list(User.objects.filter(username='e'))[0]
                roundedDecimalValue = Decimal('%.3f' % float(cleanedData[3]))
                now = str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[0:22]
                print "noise,time is ("+repr(cleanedData[2])+","+repr(now)+")"
                SensorData.objects.get_or_create(sensorType='T',value=cleanedData[0],time=now, dataNum=numDataTaken, user=falco) 
                SensorData.objects.get_or_create(sensorType='H',value=cleanedData[1],time=now, dataNum=numDataTaken, user=falco) 
                SensorData.objects.get_or_create(sensorType='N',value=cleanedData[2],time=now, dataNum=numDataTaken, user=falco)
                SensorData.objects.get_or_create(sensorType='I',value=roundedDecimalValue,time=now, dataNum=numDataTaken, user=falco)
                
                users = User.objects.exclude(username='e')
                for user in users:
                    roundedDecimalValue = Decimal('%.3f' % float(cleanedData[3])) + random.randint(-1,2)
                    SensorData.objects.get_or_create(sensorType='T',value=(Decimal(cleanedData[0])+random.randint(-5,5)),time=now, dataNum=numDataTaken, user=user) 
                    SensorData.objects.get_or_create(sensorType='H',value=(Decimal(cleanedData[1])+random.randint(-10,10)),time=now, dataNum=numDataTaken, user=user)
                    SensorData.objects.get_or_create(sensorType='N',value=(Decimal(cleanedData[2])+random.randint(0,20)),time=now, dataNum=numDataTaken, user=user)
                    SensorData.objects.get_or_create(sensorType='I',value=roundedDecimalValue,time=now, dataNum=numDataTaken, user=user)                
                print "successfully added data"
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
    return x