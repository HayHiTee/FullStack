from django.urls import path

from FullStackApp.views import Home

app_name = 'FullStackApp'

urlpatterns = [
    path('', Home.as_view(), name='home')
]