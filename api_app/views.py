from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PersonsFilter, GroupbyFilter

from django.contrib.auth.models import User
from api_app.models import (
    Sites,
    Persons,
    Log,
    Pages,
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
    PageRankDataListSerializer,
    LogSerializer,
    PagesSerializer,
    KeyWordsSerializer)

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .permissions import IsOwnerOrReadOnly

from rest_framework import viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

# from .paginations import PostLimitOffsetPagination, PostPageNumberPagination


class UsersList(ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UsersListSerializer


class UsersCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # права доступа


class UsersDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer


class UsersUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UsersDelete(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer


# ----------------------------------------------------------------------------------------------------------------------

class PersonsList(ListAPIView):
    queryset = Persons.objects.all().order_by('name')
    serializer_class = PersonsListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PersonsFilter  # для поика используесть конструкция:
    # http://127.0.0.1:8000/v1/persons/?search=Putin

    # pagination_class = PostPageNumberPagination # ограничевает вывод результата на экран

    # def get_queryset(self, *args, **kwargs):
    #     '''для поика используесть конструкция: http://127.0.0.1:8000/v1/persons/?q=Putin'''
    #     queryset_list = Persons.objects.all()
    #     query = self.request.GET.get("q")
    #     if query:
    #         queryset_list = queryset_list.filter(
    #             Q(name__icontains=query) |
    #             Q(addedBy__username__icontains=query)
    #         ).distinct()
    #     return queryset_list


class PersonsCreate(CreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'name'

    def perform_create(self, serializer):
        '''использует идентификатор текущего пользователя для поля один ко многим, автоподстановка'''
        serializer.save(addedBy=self.request.user)
        print(self.request.user)


class PersonsDetail(RetrieveAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsDitailListSerializer
    # lookup_field = 'name'


class PersonsUpdate(RetrieveUpdateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # lookup_field = 'name'

    def perform_update(self, serializer):
        '''использует идентификатор текущего пользователя для поля один ко многим, автоподстановка'''
        serializer.save(addedBy=self.request.user)


class PersonsDelete(DestroyAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # lookup_field = 'name'


# ----------------------------------------------------------------------------------------------------------------------

class SitesList(ListAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesListSerializer


class SitesCreate(CreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        '''использует идентификатор текущего пользователя для поля один ко многим, автоподстановка'''
        serializer.save(addedBy=self.request.user)


class SitesDetail(RetrieveAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesListSerializer


class SitesUpdate(RetrieveUpdateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        '''использует идентификатор текущего пользователя для поля один ко многим, автоподстановка'''
        serializer.save(addedBy=self.request.user)


class SitesDelete(DestroyAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# ----------------------------------------------------------------------------------------------------------------------

class PersonsPageRankList(ListAPIView):
    queryset = PersonsPageRank.objects.all()
    serializer_class = PersonsPageRankListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = GroupbyFilter

    def get_queryset(self):
        if self.request.GET.get('siteID'):
            self.serializer_class = PersonsPageRankGroupSerializer
        return self.queryset


class PersonsPageRankDetail(GenericAPIView):
    def get_object(self, *args, **kwargs):
        # ppr_obj = PersonsPageRank.objects.filter(personID__pk=pk)
        ppr_obj = PersonsPageRank.objects.filter(personID__pk=self.kwargs['pk'])
        if ppr_obj:
            return ppr_obj
        else:
            raise Http404

    def get(self, request, format=None, *args, **kwargs):
        serializer = PersonsPageRankListSerializer(self.get_object(self.kwargs['pk']), many=True)
        return Response(serializer.data)

    # def get_queryset(self, *args, **kwargs):
    #     if self.request.GET.get('siteID'):
    #         self.queryset = self.get_object()
    #         self.serializer_class = PersonsPageRankGroupSerializer
    #     return self.queryset


    # def get_queryset(self, *args, **kwargs):
    #     '''для поика используесть конструкция: http://127.0.0.1:8000/v1/persons/?group=siteID'''
    #     queryset_list = self.get_object(self.kwargs['pk'])
    #     query = self.request.GET.get("siteID")
    #     if query:
    #         queryset_list = queryset_list.filter(
    #             Q(pageID__siteID__id__icontains=query)
    #         ).distinct()
    #         self.serializer_class = PersonsPageRankGroupSerializer
    #     return queryset_list


# ----------------------------------------------------------------------------------------------------------------------

class PersonsPageRankDateList(ListAPIView):
    queryset = PersonsPageRank.objects.all()
    serializer_class = PageRankDataListSerializer


class PersonsPageRankDateDetail(GenericAPIView):
    pass