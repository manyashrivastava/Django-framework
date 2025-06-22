from django.urls import path
from . import views

urlpatterns = [
    path('public/', views.PublicAPI.as_view()),
    path('private/', views.PrivateAPI.as_view()),
]
