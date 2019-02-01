import string
from random import choice
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.files import File as DjangoFile
from rest_framework.authtoken.models import Token

from apps.accounts.models import Account
from apps.portfolio.models import (CleanedFile, FileSchemaJob, Mapping,
                                   Portfolio, UploadedFile, MappingRule)

from allauth.account.models import EmailAddress


def _random_string(length=10):
    return ''.join(choice(string.ascii_letters) for _ in range(length))


def create_test_account(email=None,
                        password='12345678abc',
                        is_active=True,
                        create_token=True):

    if email is None:
        email = '%s@example.com' % _random_string()

    account = Account.objects.create_user(
        email=email,
        password=password,
        is_active=is_active,
    )
    EmailAddress.objects.create(
        email=email,
        user=account,
        primary=True,
        verified=True,
    )
    if create_token:
        Token.objects.create(user=account)
    return account


def create_test_portfolio(account=None, name=None):
    if account is None:
        account = create_test_account()
    if name is None:
        name = 'Portfolio %s' % _random_string(10)

    portfolio = Portfolio.objects.create(
        account=account,
        name=name)
    return portfolio


def create_test_cleaned_file(account=None, portfolio=None, uploaded_file=None, file_file=None):
    if account is None:
        account = create_test_account()
    if portfolio is None:
        portfolio = create_test_portfolio(account=account)
    if uploaded_file is None:
        uploaded_file = UploadedFile.objects.create(
            portfolio=portfolio,
            uploaded_by=account,
            file=file_file,
        )
    if file_file is None:
        file_file = NamedTemporaryFile(dir=settings.MEDIA_ROOT)
        file_file = DjangoFile(file_file)

    return CleanedFile.objects.create(
        uploaded_by=account,
        uploaded_file=uploaded_file,
        file=file_file
    )


def create_test_file_schema_job(cleaned_file=None):
    if cleaned_file is None:
        cleaned_file = create_test_cleaned_file()
    return FileSchemaJob.objects.create(
        cleaned_file=cleaned_file
    )


def create_test_mapping(file_schema_job, associations, user=None):
    if user is None:
        user = file_schema_job.cleaned_file.uploaded_by

    mapping = Mapping.objects.create(
        file_schema_job=file_schema_job)

    for source_column, target_field in associations:
        MappingRule.objects.create(
            mapping=mapping,
            mapped_by=user,
            source_column=source_column,
            target_field=target_field)

    return mapping
