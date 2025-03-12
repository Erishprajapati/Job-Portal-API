from django.shortcuts import render
from .models import User, Job, JobSeekerProfile, JobApplication
from rest_framework import viewsets
from .serializers import JobApplicationSerializer, JobSeekerSerailzier, UserSerializer, JobViewSerializer
from rest_framework import generics

# Create your views here.
class JobView(viewsets.ModelViewSet):
    querset = Job.objects.all()
    serializer_class = JobViewSerializer

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


class JobSeekerView(viewsets.ModelViewSet):
    queryset = JobSeekerProfile.objects.get()
    serializer_class = JobSeekerSerailzier

    def perform_create(self, serializer):
        serializer.save(user= self.request.user)

class JobApplicationView(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def perform_create(self,serializer):
        serializer.save(job_seeker = self.request.user.jobseekerprofile)

