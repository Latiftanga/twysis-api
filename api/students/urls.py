from django.urls import path, include

from rest_framework.routers import DefaultRouter

from students import views

router = DefaultRouter()

router.register('classes', views.ClassViewSets)
router.register('houses', views.HouseViewSets)
router.register('guardians', views.GuardianViewSets)
router.register('students', views.StudentViewSets)

app_name = 'students'

urlpatterns = [
    path('', include(router.urls))
]
