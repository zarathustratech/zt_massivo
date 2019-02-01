from django.db import models
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Borrower, Loan, Payment, Portfolio
from .serializers import (ExpandedPortfolioSerializer, PortfolioSerializer,
                          PortfolioSourceFileSchemaSerializer,
                          CreateSourceFileSerializer)

# from .serializers import PortfolioFileSerializer, PIVAFileSerializer

# from ztslackbot import SlackBot
# from ztpreprocessing.data_pipeline import crued_pipeline, extract_column_names_raw_data, apply_mappings

# from ztdb import RedisClient

# import datetime

from .serializers import CreatePortfolioSerializer
from .serializers import CreateSourceFileSerializer
from .serializers import UpdateMappingSerializer
from .serializers import ConfirmMappingSerializer
from django.shortcuts import get_object_or_404


# -----------------------------------------------------------------------------
# CREATE PORTFOLIO
# -----------------------------------------------------------------------------
class CreatePortfolioView(CreateAPIView):
    """ STEP 1: Create `Portfolio`. """
    permission_classes = (IsAuthenticated, )
    serializer_class = CreatePortfolioSerializer

    def perform_create(self, serializer):
        return serializer.save(account=self.request.user)


class UploadSourceFileView(CreateAPIView):
    """ STEP 2: Upload `SourceFile`. """
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateSourceFileSerializer

    def perform_create(self, serializer):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['id'])
        return serializer.save(portfolio=portfolio)


class MappingUpdateView(UpdateAPIView):
    """ STEP 3: Update mapping. """
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdateMappingSerializer

    def get_object(self, *args, **kwargs):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['id'])
        return portfolio.latest_source_file


class PorfolioListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PortfolioSerializer
    model = Portfolio

    def get_queryset(self, *args, **kwargs):
        queryset = Portfolio.objects.filter(account=self.request.user)
        return queryset


class PorfolioDetailBase(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Portfolio.objects.all()
    lookup_field = 'id'

    def check_object_permissions(self, request, obj):
        super(PorfolioDetailBase, self).check_object_permissions(request, obj)
        if obj.account != request.user:
            self.permission_denied(
                request, message='Permission denied'
            )


class PortfolioRetrieveView(PorfolioDetailBase):
    serializer_class = ExpandedPortfolioSerializer


class PortfolioFileSchemaView(PorfolioDetailBase):
    serializer_class = PortfolioSourceFileSchemaSerializer


# -----------------------------------------------------------------------------
# TABLE SCHEMAS
# -----------------------------------------------------------------------------
class TableSchemasView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        def get_columns_for_class(klass):
            columns = []
            for field in klass()._meta.get_fields():
                if any([
                    field.name == 'id',
                    type(field) is models.DateTimeField,
                    type(field) is models.ForeignKey,
                ]):
                    continue
                columns.append(field.name)
            return columns

        response = {
            'loan': get_columns_for_class(Loan),
            'payment': get_columns_for_class(Payment),
            'borrower': get_columns_for_class(Borrower)
        }
        return Response(response, status=status.HTTP_200_OK)




#SLACKBOT = SlackBot('portfolio_data_upload')

# redis = RedisClient()

# class PortfolioView(APIView):
#     permission_classes = (IsAuthenticated, )
#     parser_classes = (MultiPartParser,  FormParser)

#     def get(self, request):
#         """ A list of all the portfolios the user has access to. """
#         pass

#     def post(self, request):
#         pass


# class IndexView(APIView):
#     def get(self, request, format=None):
#         return Response({'Index': 'Here will be an overview of all endpoints.'})


# class RawPortfolioFileView(APIView):
#     '''Endpoint that allows to upload a raw protfolio file.'''
#     permission_classes = (AllowAny,)

#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file_serializer = PortfolioFileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             file_path = file_serializer.data['file']
#             file_path = file_path[1:]
#             # redis.publish('new_portfolio_uploads', file_path)
#             # SLACKBOT.post_message('New dataset was upoloaded {}.'.format('xlsx'))
#             column_mapping = extract_column_names_raw_data(file_path)
#             return Response(column_mapping, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PIVAFileView(APIView):
#     '''Endpoint that allows to upload a file with fresh pivas.'''
#     parser_classes = (MultiPartParser,  FormParser)

#     def post(self, request, *args, **kwargs):
#         file_serializer = PIVAFileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response('Success!', status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ColumnMappingView(APIView):

#     def post(self, request, *args, **kwargs):
#         # ColumnMapping.objects.create(mapping=request.data)
#         loans, payments, borrowers = apply_mappings('xl_2')
#         for index, borrower in borrowers.iterrows():
#             Borrower.objects.create(external_borrower_id=borrower['external_borrower_id'], name=borrower['name'],
#                                     tax_code=borrower['tax_code'])
#             if index == 100:
#                 break
#         for index, loan in loans.iterrows():
#             borrower = Borrower.objects.filter(external_borrower_id=loan['borrower'])[0]
#             issue_date = datetime.datetime.fromtimestamp(loan['issue_date']/1000)
#             default_date = datetime.datetime.fromtimestamp(loan['default_date']/1000)
#             Loan.objects.create(external_loan_id=str(loan['external_loan_id']), borrower=borrower,
#                                 portfolio_id=str(loan['portfolio_id']), gbv=float(loan['gbv']), issue_date=issue_date,
#                                 default_date=default_date, principal=loan['principal'], loan_class=loan['loan_class'])
#             if index == 100:
#                 break
#         for index, payment in payments.iterrows():
#             loan = Loan.objects.filter(external_loan_id=payment['loan_id'])[0]
#             payment_date = datetime.datetime.fromtimestamp(payment['payment_date']/1000)
#             Payment.objects.create(loan=loan, payment_date=payment_date,
#                                    payment_amount=payment['payment_amount'])
#             if index == 100:
#                 break
#         return Response('Success!', status=status.HTTP_201_CREATED)


# class PaymentView(APIView):

#     def get(self, request):
#         payments = Payment.objects.all()[:20]
#         payments = [{'loan_id': p.loan_id.external_loan_id, 'payment_date': p.payment_date, 'payment_amount': p.payment_amount} for p in payments]
#         return Response(payments)


# class LoanView(APIView):

#     def get(self, request):
#         loans = Loan.objects.all()[:20]
#         loans = [{'loan_id': l.external_loan_id, 'portfolio_id': l.portfolio_id, 'borrower': l.borrower.external_borrower_id, 'gbv': l.gbv, 'issue_date': l.issue_date,
#                   'default_date': l.default_date, 'principal': l.principal, 'loan_class': l.loan_class} for l in loans]
#         return Response(loans)


# class BorrowerView(APIView):

#     def get(self, request):
#         borrowers = Borrower.objects.all()[:20]
#         borrowers = [{'external_borrower_id': b.external_borrower_id, 'zt_borrower_id': b.zt_borrower_id, 'name': b.name, 'tax_code': b.tax_code} for b in borrowers]
#         return Response(borrowers)


# class DummyData(APIView):
#     parser_classes = (MultiPartParser,  FormParser)

#     def get(self, request):
#         s = str()
#         from django.conf import settings
#         import os
#         path = os.path.join(settings.BASE_DIR, 'zt_app/static/dummy_data/loans.csv')
#         with open(path) as f:
#             for line in f:
#                 s += line
#         return Response(s)
