from django.contrib.auth.models import User
from api_app.models import Sites, Log, Pages, Persons, PersonsPageRank, KeyWords
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class UsersListSerializer(ModelSerializer):
    login = SerializerMethodField() # сознаем новое поле с именем login
    isadmin = SerializerMethodField() # сознаем новое поле с именем isadmin
    class Meta:
        model = User
        fields = ('id', 'login', 'email', 'isadmin')

    def get_login(self, obj):
        '''использует значение username для поля login используя SerializerMethodField'''
        return str(obj.username)

    def get_isadmin(self, obj):
        return int(obj.is_superuser)


class UsersCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

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
    addedBy = SerializerMethodField()
    class Meta:
        model = Persons
        fields = ('id', 'name', 'addedBy')

    def get_addedBy(self, obj):
        '''подменяет идентификатор значением поля username в связанном поле,
        благодаря использованию SerializerMethodField'''
        return str(obj.addedBy.username)


class PersonsDitailListSerializer(ModelSerializer):
    addedBy = SerializerMethodField()
    keywords = SerializerMethodField()
    class Meta:
        model = Persons
        fields = ('id', 'name', 'addedBy', 'keywords')


    def get_addedBy(self, obj):
        '''подменяет идентификатор значением поля username в связанном поле,
        благодаря использованию SerializerMethodField'''
        return str(obj.addedBy.username)

    def get_keywords(self, obj):
        return obj.name


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