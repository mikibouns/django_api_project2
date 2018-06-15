# from auth_app.models import User
from django.contrib.auth.models import User
from api_app.models import Sites, Log, Pages, Persons, PersonsPageRank, KeyWords
from rest_framework.serializers import ModelSerializer


class UsersListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser')


class UsersCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_superuser', 'password')

# ----------------------------------------------------------------------------------------------------------------------

class SitesListSerializer(ModelSerializer):
    class Meta:
        model = Sites
        fields = ('id', 'name', 'addedBy', 'siteDescription')


class SitesCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Sites
        fields = ('id', 'name', 'siteDescription')

# ----------------------------------------------------------------------------------------------------------------------

class PersonsListSerializer(ModelSerializer):
    class Meta:
        model = Persons
        fields = ('id', 'name', 'addedBy')


class PersonsCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Persons
        fields = ('id', 'name')

# ----------------------------------------------------------------------------------------------------------------------

class PersonsPageRankSerializer(ModelSerializer):
    class Meta:
        model = PersonsPageRank
        fields = ('id', 'PersonID', 'PageID', 'Rank')


class PagesSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = ('id', 'siteID', 'URL', 'foundDateTime', 'lastScanDate')


class KeyWordsSerializer(ModelSerializer):
    class Meta:
        model = KeyWords
        fields = ('id', 'personID', 'name')


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = ('adminID', 'action', 'logDate')