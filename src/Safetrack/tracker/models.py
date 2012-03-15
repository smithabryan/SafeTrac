from django.db import models
import datetime

SENSOR_TYPES = (
    ('H', 'Humidity'),
    ('T', 'Temperature'),
    ('N', 'Noise'),
    ('I', 'Impact'),
)

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length = 30)
    accessLevel = models.PositiveIntegerField()
    lastLogin = models.DateField()
    email = models.EmailField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100) 
    pictureName = models.CharField(max_length=100)

class SensorData(models.Model):
    sensorType = models.CharField(max_length=1, choices=SENSOR_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.CharField(max_length=30)
    dataNum = models.PositiveIntegerField()    
    user = models.ForeignKey(User)
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(SensorData, self).save(*args, **kwargs)
    
class Goal(models.Model):
    sensorType = models.CharField(max_length=1, choices=SENSOR_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=3);
    
class SafetyConstraint(models.Model):    
    sensorType = models.CharField(max_length=1, choices=SENSOR_TYPES)
    gmaxValue = models.DecimalField(max_digits=10, decimal_places=3);
    gminValue = models.DecimalField(max_digits=10, decimal_places=3);
    maxValue = models.DecimalField(max_digits=10, decimal_places=3);
    minValue = models.DecimalField(max_digits=10, decimal_places=3);
    
class Team(models.Model):
    members = models.ManyToManyField(User, related_name='workers')
    supervisor = models.ForeignKey(User, related_name='leaders')
   # goals = models.PositiveIntegerField()
   # constraints = models.ManyToOneField(SafetyConstraint)
