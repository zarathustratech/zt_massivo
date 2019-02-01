

import requests
import json
from django.core.management.base import BaseCommand

from apps.portfolio.models import PopulateJob, Loan


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'populate_job_id',
            type=int)

    def handle(self, *args, **options):
        populate_job = PopulateJob.objects.get(id=options['populate_job_id'])
        cache = {}
        for loan in Loan.objects.all():
            try:
                location = cache[loan.region]
            except KeyError:
                url = 'https://maps.googleapis.com/maps/api/geocode/json?&address=%s%%2C%%20italy' % loan.region
                resp = requests.get(url)
                print('***')
                print(resp.status_code)
                print(resp.content)
                json_resp = json.loads(resp.content)
                try:
                    location = json_resp['results'][0]['geometry']['location']
                except:
                    location = None
                cache[loan.region] = location

            if location:
                loan.latitude = location['lat']
                loan.longitude = location['lng']
                loan.save()



