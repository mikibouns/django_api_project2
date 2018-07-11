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

from api_app.models import (
    Sites,
    Persons,
    PersonsPageRank,
    KeyWords,
    Pages
)

from .serializers import (
    UsersListSerializer,
    UsersCreateUpdateSerializer,
    PersonsListSerializer,
    PersonsDetailSerializer,
    PersonsCreateUpdateSerializer,
    SitesListSerializer,
    SitesCreateUpdateSerializer,
    SitesDetailSerializer,
    PersonsPageRankListSerializer,
    PersonsPageRankGroupSerializer,
    PageRankDateListSerializer,
    KeyWordsEditSerializer,
    KeyWordsListSerializer,
    PagesCreateUpdateSerializer,
    PagesListSerializer,
)

from .permissions import (
    IsOwnerOrReadOnly,
    IsOwnerOrReadOnlyKeyWords,
    IsOwnerOrReadOnlyPages,
)

from .filters import (
    PersonsFilter,
    PersonsPageRankFilter,
    UsersFilter,
)

from .logging import LoggingMixin
from .utils import validate_json, modified_user_data


class APIRootView(APIView):

    def get(self, request):
        data = [
            {
                'api_url': request.build_absolute_uri(),
                'method': 'get',
                'comments': 'Доступные url (этот документ)'
            },
            {
                'api_url': reverse('v1:schema', request=request),
                'method': 'get',
                'comments': 'Получить схему API'
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
                'api_url': reverse('v1:pages_lc', request=request),
                'method': 'get',
                'comments': 'Получить список страниц'
            },
            {
                'api_url': reverse('v1:pages_rud', args=[1], request=request),
                'method': 'get',
                'comments': 'Получить страницу по page_id = 1'
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
                'api_url': reverse('v1:keywords_lc', request=request),
                'method': 'get',
                'comments': 'Получить список слов'
            },
            {
                'api_url': reverse('v1:keywords_rud', args=[1], request=request),
                'method': 'get',
                'comments': 'Получить слово по id'
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


class UsersViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = UsersFilter

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
        mod_data = modified_user_data(request.data)
        serializer = UsersCreateUpdateSerializer(data=mod_data)
        validate_json(serializer.fields, mod_data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            return Response({'success': 1,
                             'user_id': user.id,
                             'token_auth': Token.objects.get(user=user).key}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': 0,
                             'expection': serializer._errors,
                             'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        mod_data = modified_user_data(request.data)
        queryset = self.queryset.get(pk=kwargs.get('pk'))
        serializer = UsersCreateUpdateSerializer(queryset, data=request.data, partial=True)
        validate_json(serializer.fields, mod_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 1}, status=status.HTTP_200_OK)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        queryset = self.queryset.get(pk=kwargs.get('pk'))
        self.perform_destroy(queryset)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)


class SitesViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Sites.objects.all()
    serializer_class = SitesCreateUpdateSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'addedBy')

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
        serializer = SitesCreateUpdateSerializer(data=request.data, context={'user': request.user})
        validate_json(serializer.fields, request.data)
        if serializer.is_valid():
            site = serializer.save()
            return Response(
                {'success': 1,
                'persons_id': site.id}
                , status=status.HTTP_201_CREATED)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = SitesCreateUpdateSerializer(instance, data=request.data, partial=True) # если partial = True данные разрешено передавать по отдельности
        validate_json(serializer.fields, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 1}, status=status.HTTP_200_OK)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)


class PersonsViewSet(LoggingMixin, viewsets.ModelViewSet):
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
        serializer = PersonsDetailSerializer(person)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PersonsCreateUpdateSerializer(data=request.data)
        validate_json(serializer.fields, request.data)
        if serializer.is_valid():
            person = Persons.create(request, person=serializer.validated_data['name'])
            person.save()
            return Response(
                {'success': 1,
                'persons_id': person.id}
                , status=status.HTTP_201_CREATED
            )
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = PersonsCreateUpdateSerializer(instance, data=request.data, partial=True)
        validate_json(serializer.fields, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 1}, status=status.HTTP_200_OK)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)


class PersonsPageRankViewSet(LoggingMixin, viewsets.ReadOnlyModelViewSet):
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


class PPRDateViewSet(LoggingMixin, viewsets.ReadOnlyModelViewSet):
    queryset = PersonsPageRank.objects.all()
    serializer_class = PageRankDateListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PersonsPageRankFilter

    def groupby(self, queryset):
        request_get = self.request.GET
        if request_get.get('groupby') == 'siteID':
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


class KeyWordsViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyKeyWords]
    queryset = KeyWords.objects.all()
    serializer_class = KeyWordsEditSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Persons.objects.all())
        serializer = PersonsDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        keyword = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = KeyWordsListSerializer(keyword)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = KeyWordsEditSerializer(data=request.data)
        validate_json(serializer.fields, request.data)
        if serializer.is_valid():
            words_list = serializer.save()
            return Response(
                    {'success': 1,
                     'personID': request.data.get('personID'),
                     'added_keywords': words_list}, status=status.HTTP_201_CREATED)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        queryset = self.queryset.get(pk=kwargs.get('pk'))
        serializer = KeyWordsListSerializer(queryset, data=request.data, partial=True)
        validate_json(serializer.fields, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 1}, status=status.HTTP_200_OK)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)


class PagesViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPages]
    queryset = Pages.objects.all()
    serializer_class = PagesCreateUpdateSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Sites.objects.all())
        serializer = SitesDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        urls = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = PagesListSerializer(urls)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        validate_json(serializer.fields, request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        page_id = self.queryset.get(URL=request.data['URL'])
        return Response({'success': 1,
                         'page_id': page_id.id,
                         }, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        validate_json(serializer.fields, request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'success': 1}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 1}, status=status.HTTP_204_NO_CONTENT)