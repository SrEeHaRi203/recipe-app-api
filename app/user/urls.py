"""
URL mapping for the user API.
"""

from django.urls import path

from user import views

## noqa NOTE: This is used in test for reverse mapping --> reverse('user:create')-- create path name of user app.
app_name = 'user'

## noqa NOTE: In path django expects a function not a class so we use .as_view()
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
