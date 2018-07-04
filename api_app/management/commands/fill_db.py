from django.core.management.base import BaseCommand
from api_app.models import User, Persons, KeyWords, Pages, PersonsPageRank, Sites, Log
from data_for_testing import *


class Command(BaseCommand):
    def handle(self, *args, **options):

        User.objects.all().delete()
        for user in data_users:
            new_user = User.objects.create_user(
                username=user['username'],
                email=user['email'],
                password=user['password'],
            )
            new_user.save()

        Persons.objects.all().delete()
        for person in data_persons:
            person['addedBy'] = User.objects.get(username=person['addedBy'])
            new_person = Persons(**person)
            new_person.save()

        Sites.objects.all().delete()
        for site in data_sites:
            site['addedBy'] = User.objects.get(username=site['addedBy'])
            new_site = Sites(**site)
            new_site.save()

        Pages.objects.all().delete()
        for page in data_pages:
            page['siteID'] = Sites.objects.get(name=page['siteID'])
            new_page = Pages(**page)
            new_page.save()

        KeyWords.objects.all().delete()
        for keyword in data_keywords:
            keyword['personID'] = Persons.objects.get(name=keyword['personID'])
            new_keyword = KeyWords(**keyword)
            new_keyword.save()

        PersonsPageRank.objects.all().delete()
        for ppr in data_personspagerank:
            ppr['personID'] = Persons.objects.get(name=ppr['personID'])
            ppr['pageID'] = Pages.objects.get(URL=ppr['pageID'])
            new_personspagerank = PersonsPageRank(**ppr)
            new_personspagerank.save()

        super_user = User.objects.create_superuser('admin', 'admin@mail.com', 'admins_password')
        super_user.save()