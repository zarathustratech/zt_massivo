import traceback
import celery
import pandas as pd

from collections import defaultdict
from django.db import connection
from apps.portfolio.models import (ExtractedDataPoint, ExtractJob,
                                   FileSchemaJob, PopulateJob, InferenceJob,
                                   SourceColumn, SourceSheet, Loan)
from apps.portfolio.readers import create_reader


# -----------------------------------------------------------------------------
# ENTRY POINTS
# -----------------------------------------------------------------------------

def enqueue_file_schema_job(cleaned_file, account=None):
    job = FileSchemaJob.objects.create(
        cleaned_file=cleaned_file,
        started_by=account)
    run_file_schema_job.delay(job_id=job.id)


def enqueue_extract_job(mapping, account=None):
    job = ExtractJob.objects.create(
        mapping=mapping,
        started_by=account)
    run_extract_job.delay(job_id=job.id)


def enqueue_populate_job(extract_job, account=None):
    job = PopulateJob.objects.create(
        extract_job=extract_job,
        started_by=account)
    run_populate_job.delay(job_id=job.id)


def enqueue_inference_job(populate_job, account=None):
    job = InferenceJob.objects.create(
        populate_job=populate_job,
        started_by=account)
    run_inference_job.delay(job_id=job.id)


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def store_file_schema(file_schema_job, file_schema):
    source_columns = []
    n_sheets, n_columns = 0, 0
    for sheet_name, columns in file_schema.items():
        source_sheet = SourceSheet.objects.create(
            file_schema_job=file_schema_job,
            name=sheet_name)
        n_sheets += 1
        for col_index, column_name in columns:
            source_column = SourceColumn(
                source_sheet_name=sheet_name,
                source_sheet=source_sheet,
                index=col_index,
                name=column_name)
            source_columns.append(source_column)
            n_columns += 1
    SourceColumn.objects.bulk_create(source_columns)
    return n_sheets, n_columns


def process_payments(collections_df, time_span=120, term=1):
    n_cols = int(time_span / term)

    window_frame_df = collections_df.copy()
    del collections_df

    year_list = window_frame_df.pay_date.astype('datetime64[M]').dt.year
    month_list = window_frame_df.pay_date.astype('datetime64[M]').dt.month
    starting_year = year_list.max() - int(time_span / 12)
    last_year_rows = window_frame_df[year_list == year_list.max()]
    starting_month = last_year_rows.pay_date.astype('datetime64[M]').dt.month.max()
    window_frame_df["f"] = ((year_list - starting_year) * 12) + (month_list - starting_month)
    window_frame_df["f"] = ((window_frame_df["f"] - 1) / term) + 1
    window_frame_df["f"] = window_frame_df["f"].astype(int)
    window_frame_df = window_frame_df[(window_frame_df["f"] > 0)]

    date_frame_df = window_frame_df[['loan_id', 'amount', 'f']]
    date_frame_df['f'] = date_frame_df['f'].fillna(n_cols)
    date_frame_df['amount'] = date_frame_df['amount'].fillna(0)

    aggregated_df = date_frame_df.groupby(['loan_id', 'f']).agg({'amount': 'sum'})
    aggregated_df = aggregated_df.reset_index()

    result_df = aggregated_df.pivot(index='loan_id', columns='f', values='amount')
    result_df = result_df.reset_index()
    result_df = result_df.fillna(0)

    lineacred_gbv_df = window_frame_df[['loan_id', 'gbv']]
    outcome_df = result_df.set_index('loan_id').join(lineacred_gbv_df.set_index('loan_id'), how='left')
    outcome_df = outcome_df.drop_duplicates()
    drop_cols = {}
    for x in range(1, n_cols + 1):
        if x in outcome_df:
            drop_cols[x] = "{}".format(x)
            outcome_df["m{}".format(x)] = outcome_df[x] / outcome_df['gbv']
        else:
            outcome_df["m{}".format(x)] = outcome_df['gbv'] - outcome_df['gbv']
    outcome_df = outcome_df.drop(columns=['gbv'])
    outcome_df = outcome_df.reset_index()
    outcome_df = outcome_df.drop(columns=drop_cols)

    return outcome_df


# -----------------------------------------------------------------------------
# TASKS
# -----------------------------------------------------------------------------
@celery.task
def run_file_schema_job(job_id):
    job = FileSchemaJob.objects.get(id=job_id)
    job.start_job()
    job.save()

    # Extract file schema
    try:
        ### Getting an absolute path as it is not working with relative paths
        file_path = job.cleaned_file.file.path
        ###
        with create_reader(file_path=file_path) as reader:
            file_schema = reader.get_schema()

    except Exception as exc:
        job.finish_job_failure()
        job.logs = '[STACKTRACE]\n%s' % str(traceback.format_exc())
        job.save()
        return

    # Store in database
    try:
        n_sheets, n_columns = store_file_schema(
            file_schema_job=job,
            file_schema=file_schema)

        job.n_sheets = n_sheets
        job.n_columns = n_columns
        job.finish_job_success()
        job.save()
    except Exception as exc:
        job.finish_job_failure()
        logs = '[STACKTRACE]\n%s\n' % str(traceback.format_exc())
        logs += '[FILE SCHEMA]\n%s\n' % str(file_schema)
        job.logs = logs
        job.save()


@celery.task
def run_extract_job(job_id):
    job = ExtractJob.objects.get(id=job_id)
    job.start_job()
    job.save()

    try:
        ### Getting an absolute path as it is not working with relative paths
        file_path = job.mapping.file_schema_job.cleaned_file.file.path
        ###
        with create_reader(file_path=file_path) as reader:
            rules = job.mapping.mappingrule_set.all()
            logs = ['[EXTRACTJOB]']
            logs.append('Start reading using %s.' % reader.__class__.__name__)

            rules_by_sheet = {}
            for rule in rules:
                sheet_name = rule.source_column.source_sheet_name
                try:
                    rules_by_sheet[sheet_name].append(rule)
                except KeyError:
                    rules_by_sheet[sheet_name] = [rule]

            for sheet_name, sheet_rules in rules_by_sheet.items():
                log = '%s has %s mapping rules.' \
                      % (sheet_name, len(sheet_rules))
                logs.append(log)

            data_points = []
            n_data_points = 0

            for sheet_name, sheet_rules in rules_by_sheet.items():
                n_sheet_points = 0

                indexes = sorted(list(set(
                    [rule.source_column.index for rule in sheet_rules])))

                rules_by_col_index = {}
                for rule in sheet_rules:
                    for index, original_index in enumerate(indexes):
                        if original_index == rule.source_column.index:
                            try:
                                rules_by_col_index[index].append(rule)
                            except KeyError:
                                rules_by_col_index[index] = [rule]
                            break
                    else:
                        raise Exception

                data_frame = reader.get_data_frame(
                    sheet_name=sheet_name,
                    column_indexes=indexes)

                for row_index, row in data_frame.iterrows():
                    for col_index, value in enumerate(row):
                        for rule in rules_by_col_index[col_index]:
                            n_sheet_points += 1
                            data_point = ExtractedDataPoint(
                                extract_job=job,
                                mapping_rule=rule,
                                row_n=row_index,
                                value=value)
                            data_points.append(data_point)
                    if len(data_points) > 150:
                        ExtractedDataPoint.objects.bulk_create(data_points)
                        data_points = []
                log = 'Found in sheet "%s", %s rows with %s points.' \
                      % (sheet_name, len(data_frame), n_sheet_points)
                logs.append(log)
                n_data_points += n_sheet_points

            if len(data_points) > 0:
                ExtractedDataPoint.objects.bulk_create(data_points)

        job.finish_job_success()
        job.logs = '\n'.join(logs)
        job.n_extracted_data_points = n_data_points
        job.save()

    except Exception as exc:
        job.finish_job_failure()
        job.logs = '[STACKTRACE]\n%s' % str(traceback.format_exc())
        job.save()
        return


@celery.task
def run_populate_job(job_id):
    try:
        job = PopulateJob.objects.get(id=job_id)
        job.start_job()
        job.save()

        logs = []
        counter = defaultdict(int)

        all_rules = job.extract_job.mapping.mappingrule_set.all()

        rules_by_model = {}
        for rule in all_rules:
            model = rule.target_field.target_model.content_type.model_class()
            try:
                rules_by_model[model].append(rule)
            except KeyError:
                rules_by_model[model] = [rule]

        for model, rules in rules_by_model.items():
            row_numbers = ExtractedDataPoint.objects \
                .filter(mapping_rule__in=rules) \
                .values_list('row_n', flat=True) \
                .order_by('row_n') \
                .distinct()

            log = 'Using %s to populate %s. Found %s rows.' \
                  % (len(rules), model.__name__, len(row_numbers))
            logs.append(log)

            field_name_by_rule_id = {}
            rules_by_id = dict([(rr.id, rr) for rr in rules])

            for row_n in row_numbers:
                params = {}
                extracted_data_points = ExtractedDataPoint.objects \
                    .filter(row_n=row_n, mapping_rule__in=rules)

                for data_point in extracted_data_points:
                    rule = rules_by_id[data_point.mapping_rule_id]
                    try:
                        field_name = field_name_by_rule_id[rule.id]
                    except KeyError:
                        field_name = rule.target_field.name
                        field_name_by_rule_id[rule.id] = field_name

                    field_value = rule.cast_value(data_point.value)
                    params[field_name] = field_value

                try:
                    model.objects.create(
                        populate_job=job,
                        row_n=row_n,
                        **params)
                    counter[model.__name__] += 1
                except Exception as exc:
                    title = '\n***\nCould not create %s for row %s.' \
                            % (model.__name__, row_n)
                    logs = [title]
                    for data_point in extracted_data_points:
                        field_name = \
                            field_name_by_rule_id[data_point.mapping_rule_id]
                        field_log = '%s: %s -> %s: %s.' % \
                                    (data_point.mapping_rule.source_column,
                                     data_point.value,
                                     data_point.mapping_rule.target_field,
                                     params[field_name])
                        logs.append(field_log)

        job.finish_job_success()
        job.logs = '\n'.join(logs)
        job.n_borrowers = counter['Borrower']
        job.n_loans = counter['Loan']
        job.n_payments = counter['Payment']
        job.save()
    except Exception as exc:
        print(exc)
        job.finish_job_failure()
        job.logs = '[STACKTRACE]\n%s' % str(traceback.format_exc())
        job.save()
        return


@celery.task
def run_inference_job(job_id):
    try:
        job = InferenceJob.objects.get(id=job_id)
        job.start_job()
        job.save()

        logs = []
        populate_job_id = job.populate_job.id

        sql_query = """
                SELECT
                PL.external_loan_id,
                PL.gbv,
                PP.pay_date,
                PP.amount

                FROM portfolio_loan PL

                INNER JOIN portfolio_payment PP
                ON PP.external_loan_id = PL.external_loan_id
                AND PP.populate_job_id={job_id}

                WHERE PL.populate_job_id={job_id}
            """.format(job_id=populate_job_id)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        payments_df = pd.DataFrame(data=rows, columns=['loan_id', 'gbv', 'pay_date', 'amount'])
        monthly_payments = process_payments(payments_df)

        from apps.portfolio.mle import MachineLearningEngine
        mle = MachineLearningEngine()
        loans_rr = mle.get_ztrr(monthly_payments)
        try:
            for index, loan_rr in loans_rr.iterrows():
                loan_obj = Loan.objects.get(external_loan_id=loan_rr['loan_id'])
                loan_obj.rec_6 = loan_rr['fm+6']
                loan_obj.rec_12 = loan_rr['fm+12']
                loan_obj.rec_18 = loan_rr['fm+18']
                loan_obj.save()
        except Exception as exc:
            print(exc)
            job.finish_job_failure()
            job.logs = '\n***\nCould not update loan {}.'.format(loan_rr['loan_id'])
            job.save()
            return

        job.finish_job_success()
        job.logs = '\n'.join(logs)
        job.n_default_cases = loans_rr[loans_rr['fm+1'] > 0].shape[0]
        job.n_paid_cases = loans_rr[loans_rr['fm+1'] == 0].shape[0]
        job.mean_recovery_rate_6 = loans_rr['fm+6'].mean()
        job.mean_recovery_rate_12 = loans_rr['fm+12'].mean()
        job.mean_recovery_rate_18 = loans_rr['fm+18'].mean()
        job.save()
    except Exception as exc:
        print(exc)
        job.finish_job_failure()
        job.logs = '[STACKTRACE]\n%s' % str(traceback.format_exc())
        job.save()
        return
