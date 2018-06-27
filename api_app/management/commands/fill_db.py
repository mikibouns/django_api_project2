from django.core.management.base import BaseCommand
from api_app.models import User, Persons, KeyWords, Pages, PersonsPageRank, Sites, Log

data_users = [
    {
        'email': 'user1@mail.com',
        'password': 'userpassword',
        'username': 'user1'
    },
    {
        'email': 'user2@mail.com',
        'password': 'userpassword',
        'username': 'user2'
    },
    {
        'email': 'user3@mail.com',
        'password': 'userpassword',
        'username': 'user3'
    },
]

data_persons = [
    {
        'name': 'Путин',
        'addedBy': 'user1',

    },
    {
        'name': 'Трамп',
        'addedBy': 'user2',
    },
    {
        'name': 'Ким Чен Ын',
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
        'name': 'Путина',
        'personID': 'Путин',
    },
    {
        'name': 'Путиным',
        'personID': 'Путин',
    },
    {
        'name': 'Путину',
        'personID': 'Путин',
    },
    {
        'name': 'Путин',
        'personID': 'Путин',
    },
    {
        'name': 'Ким Чен Ыном',
        'personID': 'Ким Чен Ын',
    },
    {
        'name': 'Ким Чен Ыну',
        'personID': 'Ким Чен Ын',
    },
    {
        'name': 'Ким Чен Ын',
        'personID': 'Ким Чен Ын',
    },
    {
        'name': 'Трампом',
        'personID': 'Трамп',
    },
    {
        'name': 'Трампу',
        'personID': 'Трамп',
    },
    {
        'name': 'Трамп',
        'personID': 'Трамп',
    },
]

data_personspagerank = [
    {
        'personID': 'Путин',
        'pageID': 'https://motor.ru/',
        'rank': '10',
    },
    {
        'personID': 'Путин',
        'pageID': 'https://lenta.ru/',
        'rank': '3',
    },
    {
        'personID': 'Ким Чен Ын',
        'pageID': 'https://www.rambler.ru/',
        'rank': '12',
    },
    {
        'personID': 'Трамп',
        'pageID': 'https://motor.ru/',
        'rank': '5',
    },
]


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