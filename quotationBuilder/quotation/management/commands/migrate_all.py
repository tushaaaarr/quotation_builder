import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # input
        apps = [
            '',
            'quotation',

        ]
        databases = [
            'default',
        ]

        # make migrations
        for app in apps:
            cmd = 'python manage.py makemigrations '+app
            os.system(cmd)
            # print(subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read())

        # migrate to SQL databases
        for database in databases:
            cmd = 'python manage.py migrate --database='+database
            os.system(cmd)
            # print(subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read())