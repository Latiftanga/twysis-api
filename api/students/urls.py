from django.urls import path, include

from rest_framework.routers import DefaultRouter

from students import views

router = DefaultRouter()

router.register('classes', views.ClassViewSets)


app_name = 'students'

urlpatterns = [
    path('', include(router.urls))
]
