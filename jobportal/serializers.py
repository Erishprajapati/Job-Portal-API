from rest_framework import serializers 
from .models import User, JobApplication, JobSeekerProfile, Job


class JobViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description','salary', 'location']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_jobseeker', 'is_emplooyer']

class JobSeekerSerailzier(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['name', 'resume', 'skills', 'experience']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status', 'applied_on', 'jobseeker', 'job']

