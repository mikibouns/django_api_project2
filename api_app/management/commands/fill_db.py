from django.core.management.base import BaseCommand
from api_app.models import User, Persons, KeyWords, Pages, PersonsPageRank, Sites, Log
import json
import os
from api_project.settings import BASE_DIR


def load_from_json(file_name):
    with open(os.path.join(BASE_DIR, file_name + '.json'), encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        data_json = load_from_json('data_for_testing')

        User.objects.all().delete()
        for user in data_json['users']:
            new_user = User.objects.create_user(
                username=user['username'],
                email=user['email'],
                password=user['password'],
            )
            new_user.save()

        Persons.objects.all().delete()
        for person in data_json['persons']:
            person['addedBy'] = User.objects.get(username=person['addedBy'])
            new_person = Persons(**person)
            new_person.save()

        Sites.objects.all().delete()
        for site in data_json['sites']:
            site['addedBy'] = User.objects.get(username=site['addedBy'])
            new_site = Sites(**site)
            new_site.save()

        Pages.objects.all().delete()
        for page in data_json['pages']:
            page['siteID'] = Sites.objects.get(name=page['siteID'])
            new_page = Pages(**page)
            new_page.save()

        KeyWords.objects.all().delete()
        for keyword in data_json['keywords']:
            keyword['personID'] = Persons.objects.get(name=keyword['personID'])
            new_keyword = KeyWords(**keyword)
            new_keyword.save()

        PersonsPageRank.objects.all().delete()
        for ppr in data_json['personspagerank']:
            ppr['personID'] = Persons.objects.get(name=ppr['personID'])
            ppr['pageID'] = Pages.objects.get(URL=ppr['pageID'])
            new_personspagerank = PersonsPageRank(**ppr)
            new_personspagerank.save()

        super_user = User.objects.create_superuser('admin', 'admin@mail.com', 'admins_password')
        super_user.save()