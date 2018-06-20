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
    # addedBy = SerializerMethodField()
    keywords = SerializerMethodField()
    class Meta:
        model = Persons
        fields = ('id', 'name', 'keywords')


    # def get_addedBy(self, obj):
    #     '''подменяет идентификатор значением поля username в связанном поле,
    #     благодаря использованию SerializerMethodField'''
    #     return str(obj.addedBy.username)

    def get_keywords(self, obj):
        data = KeyWordsSerializer(obj.keywords_children(), many=True).data
        if data:
            return data
        return None


class PersonsCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Persons
        fields = ('id', 'name')


# ----------------------------------------------------------------------------------------------------------------------

class PersonsPageRankListSerializer(ModelSerializer):
    site_id = SerializerMethodField()
    class Meta:
        model = PersonsPageRank
        fields = ('id', 'personID', 'pageID', 'rank', 'site_id')

    def get_site_id(self, obj):
        return str(obj.pageID.siteID.id)


class PersonsPageRankGroupSerializer(ModelSerializer):
    person_addby = SerializerMethodField()
    person_name = SerializerMethodField()
    person_rank = SerializerMethodField()
    site_addby = SerializerMethodField()
    site_id = SerializerMethodField()
    site_name = SerializerMethodField()

    class Meta:
        model = PersonsPageRank
        fields = ('person_addby', 'person_name', 'person_rank', 'site_addby', 'site_id', 'site_name')

    def get_person_addby(self, obj):
        return str(obj.personID.id)

    def get_person_name(self, obj):
        return str(obj.personID.name)

    def get_person_rank(self, obj):
        return str(obj.rank)

    def get_site_addby(self, obj):
        return str(obj.pageID.siteID.addedBy.username)

    def get_site_id(self, obj):
        return str(obj.pageID.siteID.id)

    def get_site_name(self, obj):
        return str(obj.pageID.siteID.name)


class PageRankDataListSerializer(ModelSerializer):
    pageID = SerializerMethodField()
    siteID = SerializerMethodField()
    url = SerializerMethodField()
    personID = SerializerMethodField()
    rank = SerializerMethodField()

    class Meta:
        model = Pages
        fields = ['pageID', 'siteID', 'url', 'personID', 'rank']

    def get_pageID(self, obj):
        data = PagesGiveSerializer(obj.pages_children(), many=True).data
        if data:
            return data
        return None

    def get_siteID(self, obj):
        data = SitesListSerializer(obj.sites_children(), many=True).data
        if data:
            return data
        return None

    def get_url(self, obj):
        return str(obj.pageID.URL)

    def get_personID(self, obj):
        data = PersonsListSerializer(obj.persons_children(), many=True).data
        if data:
            return data
        return None

    def get_rank(self, obj):
        return str(obj.rank)

# ----------------------------------------------------------------------------------------------------------------------

class PagesGiveSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = ('foundDateTime', 'lastScanDate')


# ----------------------------------------------------------------------------------------------------------------------

class KeyWordsSerializer(ModelSerializer):
    class Meta:
        model = KeyWords
        fields = ('id', 'name')


# ----------------------------------------------------------------------------------------------------------------------

class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = ('adminID', 'action', 'logDate')