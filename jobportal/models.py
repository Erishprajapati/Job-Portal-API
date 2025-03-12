from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    '''User will have two category either jobseeker or emplooye'''
    is_jobseeker = models.BooleanField(default = False)
    is_emplooyer = models.BooleanField(default = False)

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=20, decimal_places=3)
    location = models.CharField(max_length=50)
    employer = models.ForeignKey(User, related_name='jobs',on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.salary} at {self.location} Description are {self.description}"

class JobSeekerProfile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(models.FileField(upload_to='resumes/'))
    skills = models.TextField()
    experience = models.TextField()

class JobApplication(models.Model):
    status_types = [
        ('A', 'Approved'),
        ('P', 'Pending'),
        ('R', 'Rejected')
    ]
    jobseeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices = status_types, default = 'P')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jobseeker} has {self.status}"

