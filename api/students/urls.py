from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from students.views import StudentViewSets, StudentGuardiansViewSets

router = DefaultRouter()
router.register('', StudentViewSets)

student_guardians_router = routers.NestedDefaultRouter(router, '', lookup='')
student_guardians_router.register('guardians', StudentGuardiansViewSets)

app_name = 'students'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(student_guardians_router.urls))
]
