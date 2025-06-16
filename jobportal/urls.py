from django.urls import path,include
from .views import *
from .models import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'jobs', JobView),
router.register(r'profiles', JobSeekerView),
router.register(r'applications', JobApplicationView)


urlpatterns = [
    path('', include(router.urls)),
]
