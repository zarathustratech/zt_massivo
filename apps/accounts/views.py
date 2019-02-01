from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import AccountSerializer


class MyAccountView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class ConfirmEmailView():
    pass