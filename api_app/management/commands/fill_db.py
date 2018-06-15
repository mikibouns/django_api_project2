from django.core.management.base import BaseCommand
from api_app.models import User, Persons, KeyWords, Pages, PersonsPageRank, Sites, Log


data_users = [
    {
        'email': 'user1@mail.com',
        'password': 'pbkdf2_sha256$36000$O1ml0WHmNSz0$vijdKCKfK8W4K1LcNxJbtPx+4CK6T2eYTBjWQz98tsU=',
        'username': 'user1',
        'is_staff': True
    },
    {
        'email': 'user2@mail.com',
        'password': 'pbkdf2_sha256$36000$O1ml0WHmNSz0$vijdKCKfK8W4K1LcNxJbtPx+4CK6T2eYTBjWQz98tsU=',
        'username': 'user2',
        'is_staff': True
    },
    {
        'email': 'user3@mail.com',
        'password': 'pbkdf2_sha256$36000$O1ml0WHmNSz0$vijdKCKfK8W4K1LcNxJbtPx+4CK6T2eYTBjWQz98tsU=',
        'username': 'user3',
        'is_staff': True
    },
]

data_persons = [
    {
        'name': 'Putin',
        'addedBy': 'user1',
    },
    {
        'name': 'Tramp',
        'addedBy': 'user2',
    },
    {
        'name': 'Obama',
        'addedBy': 'user2',
    },
]

data_sites = [
    {
        'name': 'rambler.ru',
        'addedBy': 'user1',
        'siteDescription': 'Подборка главных новостей страны и мира, которую ежедневно формируют умные роботы под присмотром очень внимательных редакторов. 2,5 тыс. источников, в том числе ведущие российские и зарубежные СМИ.'
    },
    {
        'name': 'lenta.ru',
        'addedBy': 'user2',
        'siteDescription': 'г. Москва, 115280, г. Москва, ул. Ленинская слобода, д. 19, помещение 21ФА1'
    },
    {
        'name': 'motor.ru',
        'addedBy': 'user3',
        'siteDescription': '«Мотор» — это автомобильное издание «Ленты.ру». Автомобильный журнал про машины, дороги, автогонки, про людей и для людей, которые любят машины.'
    },
]

data_pages = [
    {
        'URL': 'https://motor.ru/',
        'siteID': 'motor.ru',
    },
    {
        'URL': 'https://lenta.ru/',
        'siteID': 'lenta.ru',
    },
    {
        'URL': 'https://www.rambler.ru/',
        'siteID': 'rambler.ru',
    },
]

data_keywords = [
    {
        'name': 'igor',
        'personID': 'Putin',
    },
    {
        'name': 'sasha',
        'personID': 'Obama',
    },
    {
        'name': 'vasia',
        'personID': 'Tramp',
    },
]

data_personspagerank = [
    {
        'PersonID': 'Putin',
        'PageID': 'https://motor.ru/',
        'Rank': '10',
    },
    {
        'PersonID': 'Putin',
        'PageID': 'https://lenta.ru/',
        'Rank': '3',
    },
    {
        'PersonID': 'Putin',
        'PageID': 'https://www.rambler.ru/',
        'Rank': '12',
    },
    {
        'PersonID': 'Tramp',
        'PageID': 'https://motor.ru/',
        'Rank': '5',
    },
]


class Command(BaseCommand):
    def handle(self, *args, **options):

        User.objects.all().delete()
        for user in data_users:
            new_user = User(**user)
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
            ppr['PersonID'] = Persons.objects.get(name=ppr['PersonID'])
            ppr['PageID'] = Pages.objects.get(URL=ppr['PageID'])
            new_personspagerank = PersonsPageRank(**ppr)
            new_personspagerank.save()

        super_user = User.objects.create_superuser('admin', 'admin@mail.com', 'm1k1b0uns')
        super_user.save()


