"""
Database diagram:

┏━━━━━━━━━━━━━━━━━━┓
┃     Portfolio    ┃
┗━━━━━━━━━━━━━━━━━━┛
         ^
         |
┏━━━━━━━━━━━━━━━━━━┓
┃   UploadedFile   ┃
┗━━━━━━━━━━━━━━━━━━┛
         ^
         |
┏━━━━━━━━━━━━━━━━━━┓
┃   CleanedFile    ┃
┗━━━━━━━━━━━━━━━━━━┛
         ^
         |
┏━━━━━━━━━━━━━━━━━━┓        ┏━━━━━━━━━━━━━━━━━━┓        ┏━━━━━━━━━━━━━━━━━━┓
┃   FileSchemaJob  ┃ < ──── ┃    SourceSheet   ┃ < ──── ┃   SourceColumn   ┃
┗━━━━━━━━━━━━━━━━━━┛        ┗━━━━━━━━━━━━━━━━━━┛        ┗━━━━━━━━━━━━━━━━━━┛
         ^                                                        │
         |                                                        │
┏━━━━━━━━━━━━━━━━━━┓        ┏━━━━━━━━━━━━━━━━━━┓                  │
┃     Mapping      ┃ < ──── ┃    MappingRule   ┃  < ──────────────┤
┗━━━━━━━━━━━━━━━━━━┛        ┗━━━━━━━━━━━━━━━━━━┛                  │
         ^                                                        │
         |                                                        │
┏━━━━━━━━━━━━━━━━━━┓        ┏━━━━━━━━━━━━━━━━━━┓        ┏━━━━━━━━━━━━━━━━━━┓
┃    ExtractJob    ┃ < ──── ┃ExtractedDataPoint┃        ┃   TargetColumn   ┃
┗━━━━━━━━━━━━━━━━━━┛        ┗━━━━━━━━━━━━━━━━━━┛        ┗━━━━━━━━━━━━━━━━━━┛
         ^                            .                           .
         |                            .                           .
┏━━━━━━━━━━━━━━━━━━┓                  .                           .
┃   PopulateJob    ┃  . . . . . . . . .                           .
┗━━━━━━━━━━━━━━━━━━┛                                              .
         ^                                                        .
         ├───────────────────────────┬────────────────────────────┐
┏━━━━━━━━━━━━━━━━━━┓        ┏━━━━━━━━━━━━━━━━━━┓        ┏━━━━━━━━━━━━━━━━━━┓
┃     Borrower     ┃        ┃       Loan       ┃        ┃      Payment     ┃
┗━━━━━━━━━━━━━━━━━━┛        ┗━━━━━━━━━━━━━━━━━━┛        ┗━━━━━━━━━━━━━━━━━━┛

"""
import uuid
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
from django.urls import reverse
from apps.accounts.models import Account


class JobState:
    IDLE = 'IDLE'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'


class Job(models.Model):
    state = FSMField(default=JobState.IDLE, protected=True)
    started_by = models.ForeignKey(Account, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    logs = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @transition(field=state, source=JobState.IDLE, target=JobState.RUNNING)
    def start_job(self):
        self.started_at = timezone.now()

    @transition(field=state, source=JobState.RUNNING, target=JobState.SUCCESS)
    def finish_job_success(self):
        self.finished_at = timezone.now()

    @transition(field=state, source=JobState.RUNNING, target=JobState.FAILURE)
    def finish_job_failure(self):
        self.finished_at = timezone.now()

    class Meta:
        abstract = True


class Portfolio(models.Model):
    STATES = (
        ('UPLOADED', 'UPLOADED'),
        ('PROCESSING', 'PROCESSING'),
        ('DONE', 'DONE'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True, db_index=True,
                            null=False, blank=True)
    state = models.CharField(max_length=255, default='UPLOADED', choices=STATES)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super(Portfolio, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_admin_url(self):
        return reverse('admin:portfolio_portfolio_change', args=[self.pk])


class UploadedFile(models.Model):
    """ Raw input file given by the user. """

    uploaded_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploaded-files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return str(self.file)


class CleanedFile(models.Model):
    """ Processed uploaded file by staff or automatically. """

    uploaded_by = models.ForeignKey(Account, null=True, blank=True,
                                    on_delete=models.CASCADE)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to='cleaned-files')
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file)

    class Meta:
        get_latest_by = 'created_at'


class FileSchemaJob(Job):
    cleaned_file = models.ForeignKey(CleanedFile, on_delete=models.CASCADE)
    n_sheets = models.IntegerField(default=-1)
    n_columns = models.IntegerField(default=-1)

    class Meta:
        get_latest_by = 'created_at'

    def get_admin_url(self):
        return reverse('admin:portfolio_fileschemajob_change', args=[self.pk])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.finished_at:
            Mapping.objects.get_or_create(file_schema_job=self)


class SourceSheet(models.Model):
    """ Together with SourceColumn, they define the source file schema. """
    file_schema_job = models.ForeignKey(FileSchemaJob,
                                        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SourceColumn.objects \
            .filter(source_sheet=self) \
            .update(source_sheet_name=self.name)


class SourceColumn(models.Model):
    """
    Together with SourceSheet, they define the source file schema.
    """
    source_sheet = models.ForeignKey(SourceSheet, on_delete=models.CASCADE)
    # Denormalization for performance reasons
    source_sheet_name = models.CharField(max_length=255, null=True, blank=True)
    index = models.IntegerField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s.%s' % (self.source_sheet_name, self.name)

    class Meta:
        ordering = ('source_sheet', 'index')


class TargetModel(models.Model):
    """
    Represents a table in the database. It's original purpose was for
    Borrower, Loan & Payment.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.content_type.model

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        TargetField.objects \
            .filter(target_model=self) \
            .update(target_model_name=self.content_type.model)


class TargetField(models.Model):
    """
    The name of the field to be targeted.
    """
    target_model = models.ForeignKey(TargetModel, on_delete=models.CASCADE)
    # Denormalization for performance reasons
    target_model_name = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(
        max_length=255, help_text='Model\'s attribute, not the column name.')

    def __str__(self):
        return '%s.%s' % (self.target_model_name, self.name)

    class Meta:
        ordering = ('target_model_name', 'name')


class Mapping(models.Model):
    """
    Groups all the mapping rules.
    """
    file_schema_job = models.OneToOneField(FileSchemaJob,
                                           on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'

    def get_admin_url(self):
        return reverse('admin:portfolio_mapping_change', args=[self.pk])



class MappingRule(models.Model):
    """
    Defines a rule to take data from CleanedFile into target tables.

    Note: This is a good place to put parameters for complex rules,
    now it supports only copy, paste & cast.
    """
    mapping = models.ForeignKey(Mapping, on_delete=models.CASCADE)
    mapped_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    source_column = models.ForeignKey(SourceColumn, on_delete=models.CASCADE)
    target_field = models.ForeignKey(TargetField, on_delete=models.CASCADE)
    cast_params = models.TextField(
        null=True, blank=True, help_text='For dates we use datetime.strptime.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s -> %s' % (self.source_column, self.target_field)

    def cast_value(self, value):
        if not hasattr(self, '_cast_func'):
            model = self.target_field.target_model.content_type.model_class()
            for field in model._meta.get_fields():
                if field.name == self.target_field.name:
                    break
            else:
                raise Exception('Target field is invalid.')

            if type(field) == models.FloatField:
                cast_func = self._cast_float
            elif type(field) == models.CharField:
                cast_func = self._cast_str
            elif type(field) == models.DateField:
                cast_func = self._cast_date
            else:
                raise Exception('Not recognized field type.')
            setattr(self, '_cast_func', cast_func)
        return getattr(self, '_cast_func')(value)

    def _cast_float(self, value):
        remove_chars = ['€', '$', 'nan']
        for char in remove_chars:
            value = value.replace(char, '')
        value = value.strip()
        try:
            return float(value)
        except ValueError:
            return None

    def _cast_str(self, value):
        return str(value)

    def _cast_date(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date()
        except ValueError:
            try:
                return datetime.strptime(value, self.cast_params).date()
            except (ValueError, TypeError):
                return None


class ExtractJob(Job):
    """
    Reads CleanedFile and loads ExtractedDataPoints using a given mapping.
    """
    mapping = models.ForeignKey(Mapping, on_delete=models.CASCADE)
    n_extracted_data_points = models.IntegerField(default=-1)

    class Meta:
        get_latest_by = 'created_at'

    def get_admin_url(self):
        return reverse('admin:portfolio_extractjob_change', args=[self.pk])


class ExtractedDataPoint(models.Model):
    extract_job = models.ForeignKey(ExtractJob, on_delete=models.CASCADE)
    mapping_rule = models.ForeignKey(MappingRule, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    row_n = models.IntegerField(db_index=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('extract_job', 'mapping_rule', 'row_n')


class PopulateJob(Job):
    """
    Converts ExtractedDataPoints into rows for Borrower, Loans & Payments.
    """
    extract_job = models.ForeignKey(ExtractJob, on_delete=models.CASCADE)
    n_borrowers = models.IntegerField(default=-1)
    n_loans = models.IntegerField(default=-1)
    n_payments = models.IntegerField(default=-1)

    class Meta:
        get_latest_by = 'created_at'

    def get_admin_url(self):
        return reverse('admin:portfolio_populatejob_change', args=[self.pk])


class InferenceJob(Job):
    """
    Evaluates a portfolio data in order to get the recovery rates
    """
    populate_job = models.ForeignKey(PopulateJob, on_delete=models.CASCADE)
    n_default_cases = models.IntegerField(default=-1)
    n_paid_cases = models.IntegerField(default=-1)
    mean_recovery_rate_6 = models.FloatField(default=0)
    mean_recovery_rate_12 = models.FloatField(default=0)
    mean_recovery_rate_18 = models.FloatField(default=0)

    class Meta:
        get_latest_by = 'created_at'

    def get_admin_url(self):
        return reverse('admin:portfolio_inferencejob_change', args=[self.pk])


class OutputTable(models.Model):
    populate_job = models.ForeignKey(PopulateJob, on_delete=models.CASCADE)
    row_n = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Borrower(OutputTable):
    external_borrower_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    tax_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('populate_job', 'external_borrower_id')


class Loan(OutputTable):
    external_borrower_id = models.CharField(max_length=255, db_index=True)
    external_loan_id = models.CharField(max_length=255, db_index=True)
    external_portfolio_id = models.CharField(
        max_length=255, null=True, blank=True)
    gbv = models.FloatField()
    issue_date = models.DateField(null=True, blank=True)
    default_date = models.DateField(null=True, blank=True)
    principal = models.FloatField()
    loan_class = models.CharField(max_length=255, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)

    rec_6 = models.FloatField(null=True, blank=True)
    rec_12 = models.FloatField(null=True, blank=True)
    rec_18 = models.FloatField(null=True, blank=True)


class Payment(OutputTable):
    external_loan_id = models.CharField(max_length=255, db_index=True)
    pay_date = models.DateField()
    amount = models.FloatField()
