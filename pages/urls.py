from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("schedule/", views.schedule, name="schedule"),
    path("events/", views.events, name="events"),
    path("academy/", views.academy, name="academy"),
    path("livestream/", views.livestream, name="livestream"),
    path("contact/", views.contact, name="contact"),
]
