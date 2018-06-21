from django_filters import rest_framework as filters
from .models import Persons, PersonsPageRank


class PersonsFilter(filters.FilterSet):
    class Meta:
        model = Persons
        fields = ['id', 'name', 'addedBy']


class PersonsPageRankFilter(filters.FilterSet):
    siteID = filters.NumberFilter(name='pageID__siteID__id')
    personID = filters.NumberFilter(name='personID__id')
    pageID = filters.NumberFilter(name='pageID__id')
    _from = filters.IsoDateTimeFilter(name='pageID__foundDateTime', lookup_expr='gte')
    _till = filters.IsoDateTimeFilter(name='pageID__lastScanDate', lookup_expr='lte')

    class Meta:
        model = PersonsPageRank
        fields = ['siteID', 'personID', 'pageID', 'rank', '_from', '_till']
