from django.core.management.base import BaseCommand

from apps.portfolio.models import SourceFile
from apps.portfolio.utils import extract_file_schema


class Command(BaseCommand):
    help = 'Extracts a `SourceFile`\'s uploaded_file schema.'

    def add_arguments(self, parser):
        parser.add_argument(
            'source_file_id',
            type=int,
            help='`SourceFile` id.')

    def handle(self, *args, **options):
        source_file = SourceFile.objects.get(id=options['source_file_id'])
        schema = extract_file_schema(source_file=source_file)
        print(schema)
