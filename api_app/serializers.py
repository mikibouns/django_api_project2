# from django.contrib.auth.models import User

from auth_app.models import User
from api_app.models import Sites, Log, Pages, Persons, PersonsPageRank, KeyWords
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField
)


# Users ----------------------------------------------------------------------------------------------------------------


class UsersListSerializer(ModelSerializer):
    user_login = SerializerMethodField() # сознаем новое поле с именем login
    user_isadmin = SerializerMethodField() # сознаем новое поле с именем isadmin
    user_addedby = SerializerMethodField()
    user_email = SerializerMethodField()
    user_id = SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_id', 'user_login', 'user_email', 'user_isadmin', 'user_addedby')

    def get_user_login(self, obj):
        '''использует значение username для поля login используя SerializerMethodField'''
        return str(obj.username)

    def get_user_isadmin(self, obj):
        return int(obj.is_staff)

    def get_user_email(self, obj):
        return str(obj.email)

    def get_user_id(self, obj):
        return int(obj.id)

    def get_user_addedby(self, obj):
        if obj.addedBy:
            return int(obj.addedBy.id)
        return None


class UsersCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff')

    def create(self, validated_data):
        user = super(UsersCreateUpdateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        if validated_data.get('password', False):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

# Sites ----------------------------------------------------------------------------------------------------------------


class SitesListSerializer(ModelSerializer):
    class Meta:
        model = Sites
        fields = ('id', 'name', 'addedBy', 'siteDescription')


class SitesCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Sites
        fields = ('name', 'siteDescription')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.siteDescription = validated_data.get('siteDescription', instance.siteDescription)
        instance.save()
        return instance

class SitesDetailSerializer(ModelSerializer):
    pages = SerializerMethodField()
    site_id = SerializerMethodField()
    site_name = SerializerMethodField()

    class Meta:
        model = Sites
        fields = ('site_id', 'site_name', 'pages')

    def get_pages(self, obj):
        data = PagesDetailSerializer(obj.pages_children(), many=True).data
        if data:
            return data
        return None

    def get_site_id(self, obj):
        return int(obj.id)

    def get_site_name(self, obj):
        return str(obj.name)

# Persons --------------------------------------------------------------------------------------------------------------


class PersonsListSerializer(ModelSerializer):
    addedBy = SerializerMethodField()
    class Meta:
        model = Persons
        fields = ('id', 'name', 'addedBy')

    def get_addedBy(self, obj):
        '''подменяет идентификатор значением поля username в связанном поле,
        благодаря использованию SerializerMethodField'''
        return str(obj.addedBy.username)


class PersonsDetailSerializer(ModelSerializer):
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
        data = KeyWordsListSerializer(obj.keywords_children(), many=True).data
        if data:
            return data
        return None


class PersonsCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Persons
        fields = ('name', )


# PersonsPageRank ------------------------------------------------------------------------------------------------------

class PersonsPageRankListSerializer(ModelSerializer):
    site_id = SerializerMethodField()
    class Meta:
        model = PersonsPageRank
        fields = ('id', 'personID', 'pageID', 'rank', 'site_id')

    def get_site_id(self, obj):
        return int(obj.pageID.siteID.id)


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
        return int(obj.personID.id)

    def get_person_name(self, obj):
        return str(obj.personID.name)

    def get_person_rank(self, obj):
        return int(obj.rank)

    def get_site_addby(self, obj):
        return str(obj.pageID.siteID.addedBy.username)

    def get_site_id(self, obj):
        return int(obj.pageID.siteID.id)

    def get_site_name(self, obj):
        return str(obj.pageID.siteID.name)


class PageRankDateListSerializer(ModelSerializer):
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

# Pages ----------------------------------------------------------------------------------------------------------------


class PagesGiveSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = ('id', 'foundDateTime', 'lastScanDate')


class PagesListSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = ('id', 'URL', 'siteID')


class PagesDetailSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = ('id', 'URL')


class PagesCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = ('URL', 'siteID')

    def update(self, instance, validated_data):
        instance.URL = validated_data.get('URL', instance.URL)
        instance.siteID = validated_data.get('siteID', instance.siteID)
        instance.save()
        return instance

# KeyWords -------------------------------------------------------------------------------------------------------------


class KeyWordsListSerializer(ModelSerializer):
    class Meta:
        model = KeyWords
        fields = ('id', 'name')


class KeyWordsEditSerializer(ModelSerializer):
    keywords = CharField(required=False, allow_blank=True, max_length=100)
    class Meta:
        model = KeyWords
        fields = ('personID', 'keywords')

    def validate_keywords(self, value):
        if isinstance(value, str):
            value = value.replace(' ', '').split(',')
        return value

    def create(self, validated_data):
        words_id = []
        for word in validated_data['keywords']:
            new_word = KeyWords(name=word, personID=Persons.objects.get(id=validated_data['personID']))
            new_word.save()
            words_id.append({"id": new_word.id,
                             "name": new_word.name})
        return words_id

