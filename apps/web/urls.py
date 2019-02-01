from django.urls import path, re_path

from .views import AppView, ContactView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    re_path(r'^app/', AppView.as_view(), name='app'),
]
