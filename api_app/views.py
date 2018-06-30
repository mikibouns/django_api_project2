# from .paginations import PostLimitOffsetPagination, PostPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
# from django.contrib.auth.models import User
from auth_app.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.decorators import action, list_route, detail_route

from api_app.models import (
    Sites,
    Persons,
    PersonsPageRank,
    KeyWords)

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
    PageRankDateListSerializer,
    KeyWordsEditSerializer,
    KeyWordsListSerializer)

from .permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyKeyWords

from .filters import (
    PersonsFilter,
    PersonsPageRankFilter)


class APIRootView(APIView):
    def get(self, request):
        data = [
            {
                'api_url': request.build_absolute_uri(),
                'method': 'get',
                'comments': 'Описание доступных методов (этот документ)'
            },
            {
                'api_url': reverse('v1:users_lc', request=request),
                'method': 'get',
                'comments': 'Получить список пользователей'
            },
            {
                'api_url': reverse('v1:users_rud', args=[1], request=request),
                'method': 'get',
                'comments': 'Получить пользователя c id = 1'
            },
            {
                'api_url': reverse('v1:persons_lc', request=request),
                'method': 'get',
                'comments': 'Получить список персон'
            },
            {
                'api_url': reverse('v1:persons_rud', args=[1], request=request),
                'method': 'get',
                'comments': 'Получить ключевые слова для person_id = 1'
            },
            {
                'api_url': reverse('v1:ppr_lc', request=request),
                'method': 'get',
                'comments': 'Получить список персон с их рангами по всем сайтам'
            },
            {
                'api_url': reverse('v1:ppr_rud', args=[1], request=request),
                'method': 'get',
                'comments': 'Получить список рангов по всем сайтам для person_id = 1'
            },
            {
                'api_url': reverse('v1:sites_lc', request=request),
                'method': 'get',
                'comments': 'Получить список сайтов'
            },
            {
                'api_url': reverse('v1:sites_rud', args=[1], request=request),
                'method': 'get',
                'comments': 'Получить сайт по site_id = 1'
            },
            {
                'api_url': reverse('v1:ppr_date_lc', request=request),
                'method': 'get',
                'comments': 'Получить список персон с их рангами по всем сайтам c информацией о периоде времени'
            },
            {
                'api_url': reverse('v1:ppr_date_r', args=[1], request=request),
                'method': 'get',
                'comments': 'Получить ранг person_id=1 по всем сайтам c информацией о периоде времени'
            },
        ]
        return Response(data)


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UsersListSerializer

    def modified_data(self, data):
        mod_data = {}
        for key, value in {'username': 'user_login',
                           'email': 'user_email',
                           'password': 'user_password',
                           'is_staff': 'user_isadmin'}.items():
            for j in data.keys():
                if value == j:
                    mod_data[key] = data.get(j, None)
        return mod_data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = UsersListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = UsersListSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        mod_data = self.modified_data(request.data)
        serializer = UsersCreateUpdateSerializer(data=mod_data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            user.is_staff = True
            user.addedBy = request.user
            user.save()
            return Response(
                {'success': 1,
                 'user_id': user.id,
                 'token_auth': Token.objects.get(user=user).key}
                , status=status.HTTP_201_CREATED
            )
        return Response({
                'success': 0,
                'exception': ''
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        print(request.data)
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


class SitesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Sites.objects.all()
    serializer_class = SitesCreateUpdateSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SitesListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        site = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = SitesListSerializer(site)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = SitesCreateUpdateSerializer(data=request.data)
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


class PersonsViewSet(viewsets.ModelViewSet):
    queryset = Persons.objects.all()
    serializer_class = PersonsCreateUpdateSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filter_class = PersonsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PersonsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        person = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = PersonsDitailListSerializer(person)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PersonsCreateUpdateSerializer(data=request.data)
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


class PersonsPageRankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonsPageRank.objects.all()
    serializer_class = PersonsPageRankListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PersonsPageRankFilter

    def groupby(self, queryset):
        if self.request.GET.get('groupby') == 'siteID':
            return PersonsPageRankGroupSerializer(queryset, many=True)
        else:
            return PersonsPageRankListSerializer(queryset, many=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.groupby(queryset)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(personID__pk=kwargs.get('pk')))
        serializer = self.groupby(queryset)
        return Response(serializer.data)


class PPRDateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonsPageRank.objects.all()
    serializer_class = PageRankDateListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PersonsPageRankFilter

    def groupby(self, queryset):
        if self.request.GET.get('groupby') == 'siteID':
            return PersonsPageRankGroupSerializer(queryset, many=True)
        else:
            return PageRankDateListSerializer(queryset, many=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.groupby(queryset)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(personID__pk=kwargs.get('pk')))
        serializer = self.groupby(queryset)
        return Response(serializer.data)


class KeyWordsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyKeyWords]
    queryset = KeyWords.objects.all()
    serializer_class = KeyWordsEditSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PersonsDitailListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        keyword = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = KeyWordsListSerializer(keyword)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            person = Persons.objects.get(id=request.data['personID'])
            if person.addedBy == request.user or request.user.is_superuser:
                words_list = KeyWords.create(request,
                                       words=request.data['keywords'],
                                       person=person)
                return Response(
                    {'success': 1,
                     'personID': person.id,
                     'added_keywords': words_list}
                    , status=status.HTTP_201_CREATED
                )
            return Response({
                'success': 0,
                'exception': 'You do not have permission to perform this action.'
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'success': 0,
                'exception': e
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = KeyWordsListSerializer(instance, data=request.data, partial=True)
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
