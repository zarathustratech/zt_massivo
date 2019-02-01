from django.urls import include, path
from django.views.generic import TemplateView
from allauth.account.views import confirm_email
from . import views

from rest_auth.registration import urls
urlpatterns = [
    path('me/', views.MyAccountView.as_view()),
    path('auth/', include('rest_auth.urls')),
    path('auth/register/account-confirmation-sent/',
         TemplateView.as_view(template_name='account/email_confirmation_sent.html'),
         name='account_email_verification_sent'
    ),
    path('auth/register/account-confirm-email/<str:key>/',
         confirm_email,
         name='account_confirm_email'),
    path('auth/register/', include('rest_auth.registration.urls')),
]
