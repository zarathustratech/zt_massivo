from rest_framework import serializers

from apps.portfolio.models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    n_loans = serializers.SerializerMethodField('count_loans')

    class Meta:
        model = Portfolio
        fields = (
            'account',
            'name',
            'code',
            'state',
            'n_loans',
            'created_at',
            'updated_at')

    def count_loans(self, portfolio):
        try:
            uploaded_file = portfolio.uploadedfile_set.all().latest()
            cleaned_file = uploaded_file.cleanedfile_set.all().latest()
            file_schema_job = cleaned_file.fileschemajob_set.all().latest()
            extract_job = file_schema_job.mapping.extractjob_set.all().latest()
            populate_job = extract_job.populatejob_set.all().latest()
            return populate_job.loan_set.count()
        except Exception as exc:
            print(exc)
            return None

class CreatePortfolioSerializer(serializers.Serializer):
    file = serializers.FileField()


class PortfolioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = (
            'account',
            'name',
            'code',
            'state',
            'created_at',
            'updated_at')
