from django.db import models

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

class SensorData(models.Model):
    sensorType = models.CharField(max_length=1, choices=SENSOR_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DateField()
    user = models.ForeignKey(User)
    
class Goal(models.Model):
    sensorType = models.CharField(max_length=1, choices=SENSOR_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=3);
    
class SafetyConstraint(models.Model):    
    sensorType = models.CharField(max_length=1, choices=SENSOR_TYPES)
    maxValue = models.DecimalField(max_digits=10, decimal_places=3);
    minValue = models.DecimalField(max_digits=10, decimal_places=3);
    
class Team(models.Model):
    members = models.ManyToManyField(User, related_name='workers')
    supervisor = models.ForeignKey(User, related_name='leaders')
    goals = models.PositiveIntegerField()
    constraints = models.PositiveIntegerField()