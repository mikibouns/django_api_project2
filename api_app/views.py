from django_filters.rest_framework import DjangoFilterBackend
from .filters import (
    PersonsFilter,
    PersonsPageRankFilter)

from django.contrib.auth.models import User
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
    PageRankDataListSerializer)

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework.response import Response

# from .paginations import PostLimitOffsetPagination, PostPageNumberPagination


# class UsersList(ListAPIView):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UsersListSerializer
#
#
# class UsersCreate(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UsersCreateUpdateSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]  # права доступа
#
#
# class UsersDetail(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UsersListSerializer
#
#
# class UsersUpdate(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UsersCreateUpdateSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]
#
#
# class UsersDelete(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UsersListSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route, list_route, action
from rest_framework import permissions, status, viewsets, views
from rest_framework.parsers import JSONParser


class UsersViewSet(viewsets.ViewSet):

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
        serializer = UsersCreateUpdateSerializer(data=request.data)
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
                'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)



class SitesViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Sites.objects.all()
        serializer = SitesListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Sites.objects.all()
        site = get_object_or_404(queryset, pk=pk)
        serializer = SitesListSerializer(site)
        return Response(serializer.data)


class PersonsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Persons.objects.all()
        serializer = PersonsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Persons.objects.all()
        person = get_object_or_404(queryset, pk=pk)
        serializer = PersonsDitailListSerializer(person)
        return Response(serializer.data)


class PersonsPageRankViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = PersonsPageRank.objects.all()
        serializer = PersonsPageRankListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PersonsPageRank.objects.filter(personID__pk=pk)
        if self.request.GET.get('groupby') == 'siteID':
            serializer = PersonsPageRankGroupSerializer(queryset, many=True)
        else:
            serializer = PersonsPageRankListSerializer(queryset, many=True)
        return Response(serializer.data)


# class PersonsPageRankDateViewSet(viewsets.ModelViewSet):
#     queryset = PersonsPageRank.objects.all()
#     serializer_class = PageRankDataListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filter_class = PersonsPageRankFilter
#
#     def groupby(self, queryset):
#         if self.request.GET.get('groupby') == 'siteID':
#             return PersonsPageRankGroupSerializer(queryset, many=True)
#         else:
#             return PageRankDataListSerializer(queryset, many=True)
#
#     def list(self, request):
#         queryset = PersonsPageRank.objects.all()
#         serializer = self.groupby(queryset)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = PersonsPageRank.objects.filter(personID__pk=pk)
#         serializer = self.groupby(queryset)
#         return Response(serializer.data)
