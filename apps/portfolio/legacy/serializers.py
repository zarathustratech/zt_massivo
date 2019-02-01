from django.db import transaction
from rest_framework import serializers

from apps.portfolio.models import (Portfolio, SourceColumn, UploadedFile,
                                   SourceSheet)
# from apps.portfolio.fileschema import populate_source_fields


# -----------------------------------------------------------------------------
# CREATE PORTFOLIO
# -----------------------------------------------------------------------------
class CreatePortfolioSerializer(serializers.ModelSerializer):
    """ STEP 1: Create `Portfolio`.  """
    class Meta:
        model = UploadedFile
        fields = ('uploaded_file', )

    def save(self, account, **kwargs):
        name = 'some name'  # get from file name
        with transaction.atomic():
            portfolio = Portfolio.objects.create(account=account)
            source_file = super(CreatePortfolioSerializer, self) \
                .save(portfolio=portfolio)



class CreateSourceFileSerializer(serializers.ModelSerializer):
    """ STEP 2: Upload `SourceFile`. """
    class Meta:
        model = UploadedFile
        fields = ('uploaded_file', 'uploaded_file_remarks')

    def save(self, portfolio, **kwargs):
        with transaction.atomic():
            source_file = super(CreateSourceFileSerializer, self)\
                .save(portfolio=portfolio, **kwargs)
            # populate_source_fields(source_file=source_file)


class UpdateMappingSerializer(serializers.ModelSerializer):
    """ STEP 3: Update mapping. """
    class Meta:
        model = UploadedFile
        fields = ('mapping', )


class ConfirmMappingSerializer(serializers.ModelSerializer):
    """ STEP 4: Confirm mapping. """
    class Meta:
        model = Portfolio
        fields = ('is_confirmed')


# -----------------------------------------------------------------------------
# LIST PORTFOLIO
# -----------------------------------------------------------------------------
class PortfolioSerializer(serializers.ModelSerializer):

    def current_step(self, obj):
        if not obj.latest_source_file.is_valid:
            return 1
        if not obj.latest_source_file.has_mapping:
            return 2
        if not obj.latest_source_file:
            return 3

    class Meta:
        model = Portfolio
        fields = (
            'code',
            # 'n_loans',
            # 'n_borrowers',
            # 'n_payments',
            # 'has_mapping',
            # 'is_confirmed',
            # 'is_file_valid',
        )


class SourceFileSerializer(serializers.ModelSerializer):
    n_loans = serializers.SerializerMethodField('count_loans')
    n_borrowers = serializers.SerializerMethodField('count_borrowers')
    n_payments = serializers.SerializerMethodField('count_payments')
    has_mapping = serializers.SerializerMethodField('mapping_saved')

    class Meta:
        model = UploadedFile
        read_only_fields = '__all__'

    def count_loans(self, obj):
        return obj.loan_set.count()

    def count_borrowers(self, obj):
        return obj.borrower_set.count()

    def count_payments(self, obj):
        return obj.payment_set.count()

    def mapping_saved(self, obj):
        return bool(obj.mapping)


class ExpandedPortfolioSerializer(PortfolioSerializer):

    pass


class CreateSourceFileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('uploaded_file', 'uploaded_file_remarks')

    def save(self, portfolio, **kwargs):
        with transaction.atomic():
            source_file = super(SourceFileSerializer, self)\
                .save(portfolio=portfolio, **kwargs)

            file_schema = extract_file_schema(source_file=source_file)

            for sheet_name, column_names in file_schema.items():
                source_sheet = SourceSheet.objects.create(
                    source_file=source_file,
                    name=sheet_name)
                source_columns = []
                for column_name in column_names:
                    source_columns.append(SourceColumn(
                        source_sheet=source_sheet,
                        name=column_name
                    ))
                SourceColumn.objects.bulk_create(source_columns)

    @property
    def data(self):
        if hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
            msg = (
                'When a serializer is passed a `data` keyword argument you '
                'must call `.is_valid()` before attempting to access the '
                'serialized `.data` representation.\n'
                'You should either call `.is_valid()` first, '
                'or access `.initial_data` instead.'
            )
            raise AssertionError(msg)

        if not hasattr(self, '_data'):
            if self.instance.portfolio:
                portfolio_serializer = PortfolioSerializer(
                    instance=self.instance.portfolio)
                self._data = portfolio_serializer.data
            else:
                return

        return self._data


class PortfolioSourceFileSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio

    @property
    def data(self):
        if not hasattr(self, '_data'):
            sheets = self.instance.latest_source_file.sourcesheet_set.all()
            data = {}
            for sheet in sheets:
                data[sheet.name] = [column.name for column
                                    in sheet.sourcecolumn_set.all()]

            self._data = data

        return self._data
