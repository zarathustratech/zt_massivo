# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import connection, migrations


def load_target_table_and_columns(apps, schema_editor):
    TargetModel = apps.get_model('portfolio', 'TargetModel')
    TargetField = apps.get_model('portfolio', 'TargetField')

    def insert_data(model_class, fields):
        ct = ContentType.objects.get_for_model(model_class)
        tm = TargetModel.objects.create(content_type_id=ct.id)
        for field in fields:
            TargetField.objects.create(
                target_model_name=tm.content_type.model,
                target_model=tm,
                name=field)

    Borrower = apps.get_model('portfolio', 'Borrower')
    borrower_fields = [
        'external_borrower_id',
        'name',
        'tax_code']
    insert_data(Borrower, borrower_fields)

    Loan = apps.get_model('portfolio', 'Loan')
    borrower_fields = [
        'external_loan_id',
        'external_borrower_id',
        'external_portfolio_id',
        'gbv',
        'issue_date',
        'default_date',
        'principal',
        'loan_class',
        'latitude',
        'longitude',
        'region']
    insert_data(Loan, borrower_fields)

    Payment = apps.get_model('portfolio', 'Payment')
    payment_fields = [
        'external_loan_id',
        'pay_date',
        'amount']
    insert_data(Payment, payment_fields)


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_target_table_and_columns),
    ]
