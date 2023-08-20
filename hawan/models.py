from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

POSITION_CHOICES = (
    ('main', 'main'),
    ('waiting', 'waiting'),
)
STATUS_CHOICES = (
    ('cancelled','cancelled'),
    ('live','live'),
)

FAMILY_MEMBERS_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
)
GENDER_CHOICES = (
    ('male','male'),
    ('female','female'),
    ('other','other'),
)
# class Id_Type(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name

ID_CHOICES = (
    ('aadhar','aadhar'),
    ('voterId','voterId'),
    ('drivingLicense','drivingLicense'),
    ('passport','passport'),
    ('other','other'),
)
class Province(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class District(models.Model):
   name = models.CharField(max_length = 100)
   province = models.ForeignKey(Province,on_delete=models.SET_NULL,blank=True,null=True,related_name='distric_province',)
   class Meta:
        ordering = ['name']
        
   def __str__(self):
       return self.name

class Event(models.Model):
    event_date = models.DateField()

    def has_excessive_participants(self):
        return (
            Participant.objects.filter(event=self, status='main').count() >= 1
            and Participant.objects.filter(event=self, status='waiting').count() >= 2
        )
    def __str__(self):
        return str(self.event_date)

class EventManager(models.Model):
    event_manager = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.event_manager.username

class Participant(models.Model):
    date_entry = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(default=18)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6,default='male')
    phone = models.CharField(max_length=15)
    state = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    village = models.CharField(max_length=100)
    type_id = models.CharField(choices=ID_CHOICES,max_length=20,default='aadhar')
    number_id = models.CharField(max_length=50)
    family_members = models.PositiveSmallIntegerField(default=0)
    position = models.CharField(choices=POSITION_CHOICES,max_length=7,default='main')
    status = models.CharField(choices=STATUS_CHOICES, max_length=9, default='live')
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6,default='')
    age = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
            return self.name if self.name else "Unnamed Family Member"