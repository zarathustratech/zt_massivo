import pandas as pd
import numpy as np
from io import StringIO

from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.portfolio.models import Portfolio, UploadedFile
from apps.portfolio.serializers import (CreatePortfolioSerializer,
                                        PortfolioDetailSerializer,
                                        PortfolioSerializer)


class PortfolioListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PortfolioSerializer
        if self.request.method == 'POST':
            return CreatePortfolioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        portfolio = self.perform_create(serializer)
        obj_serializer = PortfolioSerializer(portfolio)
        headers = self.get_success_headers(obj_serializer.data)
        return Response(
            obj_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def perform_create(self, serializer):
        portfolio = Portfolio.objects.create(
            account=self.request.user,
            name='Unnamed')
        UploadedFile.objects.create(
            uploaded_by=self.request.user,
            portfolio=portfolio,
            file=serializer.validated_data['file'])
        return portfolio

    def get_queryset(self):
        return Portfolio.objects \
            .filter(account=self.request.user) \
            .order_by('-created_at')


class PortfolioRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PortfolioDetailSerializer
    queryset = Portfolio.objects.all()
    lookup_field = 'code'

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if obj.account != request.user:
            self.permission_denied(request, message='Permission denied')

    permission_classes = (IsAuthenticated,)
    serializer_class = PortfolioDetailSerializer
    queryset = Portfolio.objects.all()
    lookup_field = 'code'

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if obj.account != request.user:
            self.permission_denied(request, message='Permission denied')


class LoanListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        try:
            portfolio = Portfolio.objects.get(code=self.kwargs['code'])
            uploaded_file = portfolio.uploadedfile_set.all().latest()

            # Dev environment
            #file_path = uploaded_file.file.path
            #uploaded_df = pd.read_csv(file_path)

            # Digital Ocean environments
            file_field = uploaded_file.file
            s = str(file_field.read(), 'utf-8')
            data = StringIO(s)
            uploaded_df = pd.read_csv(data)
            dashboard_df = uploaded_df[['cd_ngr', 'ty_cliente', 'dt_ini_fase_x', 'dt_fine_fase_x', 'im_saldo_ini',
                                        'im_int_mora_ini', 'im_saldo_netto_mora_ini', 'im_gar_reali_ini',
                                        'im_gar_person_ini', 'im_gar_altre_ini', 'fg_cli_forb_ini']]

            headers = [
                'ngr_cd',
                'cli_type',
                'init_date',
                'end_date',
                'init_balance',
                'default_interest',
                'net_balance',
                'real_guarantee',
                'personal_guarantee',
                'other_guarantee',
                'flag_forb',
            ]
            csv_rows = [','.join(headers)]

            rows = [tuple(x) for x in dashboard_df.values]
            for row in rows:
                csv_row = "%i,%s,%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%i" % row
                csv_rows.append(csv_row)

            return Response(
                data='\n'.join(csv_rows),
                content_type='application/csv',
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            print(exc)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
