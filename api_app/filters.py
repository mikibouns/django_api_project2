from django_filters import rest_framework as filters
from .models import Persons, PersonsPageRank


class PersonsFilter(filters.FilterSet):
    class Meta:
        model = Persons
        fields = ['id', 'name', 'addedBy']


class GroupbyFilter(filters.FilterSet):
    siteID = filters.NumberFilter(name='pageID__siteID__id')

    class Meta:
        model = PersonsPageRank
        fields = ['siteID', ]


class DateTimeFilter(filters.FilterSet):
    _from = filters.DateTimeFilter(name='foundDateTime')
    _till = filters.DateTimeFilter(name='lastScanDate')

    class Meta:
        model = PersonsPageRank
        fields = ['_from', '_till']