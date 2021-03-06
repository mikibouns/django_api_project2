from django_filters import rest_framework as filters
from .models import Persons, PersonsPageRank, KeyWords, Pages
from auth_app.models import User


class KeyWordsFilter(filters.FilterSet):
    name = filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = KeyWords
        fields = ['name']


class UsersFilter(filters.FilterSet):
    user_login = filters.CharFilter(name='username')
    user_email = filters.CharFilter(name='email')
    user_isadmin = filters.BooleanFilter(name='is_staff')
    user_addedby = filters.NumberFilter(name='addedBy')

    class Meta:
        model = User
        fields = ['user_login', 'user_email', 'user_isadmin', 'user_addedby']


class PersonsFilter(filters.FilterSet):
    class Meta:
        model = Persons
        fields = ['name', 'addedBy']


class PersonsPageRankFilter(filters.FilterSet):
    siteID = filters.NumberFilter(name='pageID__siteID__id')
    personID = filters.NumberFilter(name='personID__id')
    pageID = filters.NumberFilter(name='pageID__id')
    _from = filters.IsoDateTimeFilter(name='pageID__foundDateTime', lookup_expr='gte')
    _till = filters.IsoDateTimeFilter(name='pageID__lastScanDate', lookup_expr='lte')

    class Meta:
        model = PersonsPageRank
        fields = ['siteID', 'personID', 'pageID', 'rank', '_from', '_till']


class PagesFilter(filters.FilterSet):
    class Meta:
        model = Pages
        fields = ['URL', 'siteID']