from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path('create/', views.UserCreateAPIView.as_view(), name='create'),
    path('token/', views.CreateTokenAPIView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
