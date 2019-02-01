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
            file_field = uploaded_file.file
            s = str(file_field.read(), 'utf-8')
            data = StringIO(s)
            uploaded_df = pd.read_csv(data)
            dashboard_df = uploaded_df[['cd_ngr_unif', 'status', 'num_events', 'prediction', 'confidence_score',
                                        'im_acc_cassa', 'im_util_cassa', 'util_rate', 'latitude', 'longitude']]

            coord_idxs = np.random.randint(low=0, high=10, size=dashboard_df.shape[0])
            ten_italy_coordinates = [[43.769562, 11.255814],
                                     [37.075474, 15.286586],
                                     [45.438759, 12.327145],
                                     [41.902782, 12.496366],
                                     [42.349850, 13.399509],
                                     [40.725925, 8.555683],
                                     [41.230618, 16.293224],
                                     [43.880852, 10.775525],
                                     [43.548473, 10.310567],
                                     [44.414165, 8.942184]]

            rows = []
            for index, row in dashboard_df.iterrows():
                idx = coord_idxs[index]
                row['latitude'] = ten_italy_coordinates[idx][0]
                row['longitude'] = ten_italy_coordinates[idx][1]
                rows.append(tuple(row))

            headers = [
                'ngr_cd',
                'status',
                'num_events',
                'prediction',
                'confidence_score',
                'im_acc_cassa',
                'im_util_cassa',
                'util_rate',
                'latitude',
                'longitude',
            ]
            csv_rows = [','.join(headers)]
            for row in rows:
                csv_row = "%i,%i,%i,%i,'%i','%.2f','%.2f','%f',%f,%f" % row
                csv_rows.append(csv_row)

            return Response(
                data='\n'.join(csv_rows),
                content_type='application/csv',
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            print(exc)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
