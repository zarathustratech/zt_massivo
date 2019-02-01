from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from apps.accounts.models import Account


class RegisterAccountSerializer(RegisterSerializer):
    company = serializers.CharField(
        required=True,
        label="Company"
    )
    first_name = serializers.CharField(
        required=True,
        label="First name"
    )
    last_name = serializers.CharField(
        required=True,
        label="Last name"
    )

    def custom_signup(self, request, user):
        user.company = self.validated_data.get('company')
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.save()


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'company')
