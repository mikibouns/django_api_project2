# from .paginations import PostLimitOffsetPagination, PostPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route, list_route, action
from rest_framework import permissions, status, viewsets, mixins

from api_app.models import (
    Sites,
    Persons,
    PersonsPageRank)

from .serializers import (
    UsersListSerializer,
    UsersCreateUpdateSerializer,
    PersonsListSerializer,
    PersonsDitailListSerializer,
    PersonsCreateUpdateSerializer,
    SitesListSerializer,
    SitesCreateUpdateSerializer,
    PersonsPageRankListSerializer,
    PersonsPageRankGroupSerializer,
    PageRankDataListSerializer,
    KeyWordsSerializer)

from .permissions import IsOwnerOrReadOnly


from .filters import (
    PersonsFilter,
    PersonsPageRankFilter)


class UsersViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer

    def modified_data(self, data):
        mod_data = {}
        for key, value in {'username': 'user_login',
                           'email': 'user_email',
                           'password': 'user_password',
                           'is_superuser': 'isAdmin'}.items():
            for j in data.keys():
                if value == j:
                    mod_data[key] = data.get(j, None)
        return mod_data

    def list(self, request):
        queryset = User.objects.all()
        serializer = UsersListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UsersListSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        mod_data = self.modified_data(request.data)
        serializer = UsersCreateUpdateSerializer(data=mod_data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            user.is_staff = True
            user.save()
            return Response(
                {'success': 1,
                'user_id': user.id}
                , status=status.HTTP_201_CREATED
            )
        return Response({
                'success': 0,
                'exception': ''
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        mod_data = self.modified_data(request.data)
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = UsersCreateUpdateSerializer(instance, data=mod_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success': 1}
                , status=status.HTTP_201_CREATED
            )
        return Response({
            'success': 0,
            'exception': serializer.ValidationError
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        try:
            self.perform_destroy(instance)
        except Exception as e:
            return Response({'success': 0, 'exception': e}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)


class SitesViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Sites.objects.all()
    serializer_class = SitesCreateUpdateSerializer

    def list(self, request):
        queryset = Sites.objects.all()
        serializer = SitesListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Sites.objects.all()
        site = get_object_or_404(queryset, pk=pk)
        serializer = SitesListSerializer(site)
        return Response(serializer.data)

    def create(self, request):
        serializer = SitesCreateUpdateSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            site = Sites.create(request,
                                  name=serializer.validated_data['name'],
                                  siteDesc=serializer.validated_data['siteDescription'])
            site.save()
            return Response(
                {'success': 1,
                'persons_id': site.id}
                , status=status.HTTP_201_CREATED
            )
        return Response({
            'success': 0,
            'exception': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = SitesCreateUpdateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success': 1}
                , status=status.HTTP_201_CREATED
            )
        return Response({
            'success': 0,
            'exception': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        try:
            self.perform_destroy(instance)
        except Exception as e:
            return Response({'success': 0, 'exception': e}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)


class PersonsViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Persons.objects.all()
    serializer_class = PersonsCreateUpdateSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PersonsFilter

    def list(self, request):
        queryset = Persons.objects.all()
        serializer = PersonsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Persons.objects.all()
        person = get_object_or_404(queryset, pk=pk)
        serializer = PersonsDitailListSerializer(person)
        return Response(serializer.data)

    def create(self, request):
        serializer = PersonsCreateUpdateSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            person = Persons.create(request, person=serializer.validated_data['name'])
            person.save()
            return Response(
                {'success': 1,
                'persons_id': person.id}
                , status=status.HTTP_201_CREATED
            )
        return Response({
            'success': 0,
            'exception': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = PersonsCreateUpdateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success': 1}
                , status=status.HTTP_201_CREATED
            )
        return Response({
            'success': 0,
            'exception': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        try:
            self.perform_destroy(instance)
        except Exception as e:
            return Response({'success': 0, 'exception': e}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)


class PersonsPageRankViewSet(viewsets.GenericViewSet):
    queryset = PersonsPageRank.objects.all()
    serializer_class = PersonsPageRankListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PersonsPageRankFilter

    def groupby(self, queryset):
        if self.request.GET.get('groupby') == 'siteID':
            return PersonsPageRankGroupSerializer(queryset, many=True)
        else:
            return PersonsPageRankListSerializer(queryset, many=True)

    def list(self, request):
        queryset = PersonsPageRank.objects.all()
        serializer = self.groupby(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PersonsPageRank.objects.filter(personID__pk=pk)
        serializer = self.groupby(queryset)
        return Response(serializer.data)


class KeyWordsViewSet():
    pass