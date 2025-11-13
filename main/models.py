from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Administrator'),
    )
    
    POSITION_TYPE_CHOICES  = (
        ('Adviser', 'Adviser'),
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('PIO', 'PIO'),
        ('No Position', 'No Position'),
    )
    
    def generate_user_id():
        return f"{uuid4().hex[:9]}"
    
    user_id = models.CharField(default=generate_user_id, editable=False, max_length=9)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    position = models.CharField(max_length=20, choices=POSITION_TYPE_CHOICES, default="No Position")
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name="organization", null=True, blank=True)
    
    def __str__(self):
        return f"{self.user_id} - {self.username} - {self.position}" 

class Document(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    who_uploaded = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.uploaded_at}"

class Organization(models.Model):
    STATUS_CHOICES = (
        ('Operating','Operating'),
        ('Dis-banned','Dis-banned'),
    )
    
    org_name = models.CharField(default="", max_length=300)
    org_adviser = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="adviser", null=True, blank=True) 
    date_created = models.DateField(auto_now_add=False, null=True)
    org_status = models.CharField(max_length=25, choices=STATUS_CHOICES)

    def clean(self):
        if self.org_status == 'Operating' and not self.org_adviser:
            raise ValidationError({'org_adviser': 'Operating organizations must have an adviser.'})
        if self.org_adviser and self.org_adviser.user_type != 'teacher':
            raise ValidationError({'org_adviser': 'The organization adviser must be a teacher user type.'})

        
    def __str__(self):
        return f"{self.org_name}"

class Budget(models.Model):
    
    STATUS = (
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Pending', 'Pending'),
    )
    
    amount = models.IntegerField(default=0)
    request_status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    who_requested = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    date_budget_requested = models.DateTimeField(auto_now_add=True, null=True)

    def clean(self):
        user = self.who_requested
        if not user:
            raise ValidationError({'who_requested': 'Requester not set.'})
        
        if user.user_type != 'teacher' and user.position != 'Treasurer':
            raise ValidationError({'who_requested': 'You cannot request...'})


    
    def __str__(self):
        return f"{self.amount} - {self.who_requested.username} - {self.date_budget_requested}"

class Events(models.Model):
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    )
    
    event_name = models.CharField(max_length=500, default="")
    event_date = models.DateTimeField(null=True, auto_now_add=False)
    project_design_file = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    buget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, blank=True)
    event_status = models.CharField(max_length=20, default="Pending", choices=STATUS_CHOICES)
    organization_name = models.ForeignKey('Organization', on_delete=models.CASCADE)
    slug_name = models.SlugField(unique=True, max_length=200, editable=False)
    
    
    def __str__(self):
        return f"{self.event_name} - {self.event_status} - {self.organization_name.org_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.event_name)
        super().save(*args, **kwargs)


class EventAttendance(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    attendee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_time_attended = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        unique_together = ('event', 'attendee')

    def __str__(self):
        return f"{self.event.event_name} - {self.attendee.username} - {self.date_time_attended}"