from django.core.management.base import BaseCommand
from subprocess import call
import os
import re


class Command(BaseCommand):
    def create_db(self):
        try:
            call('python manage.py makemigrations && python manage.py migrate', shell=True)
        except Exception as e:
            print(e)

    def files_searcher(self, tamplate):
        home_path = os.getcwd()
        pattern = re.compile(tamplate)
        for root, _, files in os.walk(home_path):
            depth = root.count('\\') - home_path.count('\\')
            for file in files:
                if pattern.findall(file) and depth <= 3:
                    yield os.path.join(root, file)
                else:
                    yield False

    def delete_db(self):
        pattern = [r'\d\d\d\d_\w+\.py', r'^\w+\.sqlite3$']
        for template in pattern:
            for file_path in self.files_searcher(template):
                if file_path:
                    print('{} is removed'.format(file_path))
                    os.remove(file_path)

    def handle(self, *args, **options):
        self.delete_db()
        self.create_db()
