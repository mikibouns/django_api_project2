from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
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
    PersonsCreateUpdateSerializer,
    SitesListSerializer,
    SitesCreateUpdateSerializer,
    LogSerializer,
    PersonsPageRankSerializer,
    PagesSerializer,
    KeyWordsSerializer)

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

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)


class UsersList(ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UsersListSerializer


class UsersCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]# права доступа


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
    queryset = Persons.objects.all()
    serializer_class = PersonsListSerializer
    filter_backends = [SearchFilter, OrderingFilter] # для поика используесть конструкция:
    # http://127.0.0.1:8000/v1/persons/?search=Putin
    search_fields = ['name']# поля поиска
    pagination_class = LimitOffsetPagination # ограничевает вывод результата на экран

    def get_queryset(self, *args, **kwargs):
        '''для поика используесть конструкция: http://127.0.0.1:8000/v1/persons/?q=Putin'''
        queryset_list = Persons.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query) |
                Q(addedBy__username__icontains=query)
            ).distinct()
        return queryset_list


class PersonsCreate(CreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        '''использует идентификатор текущего пользователя для поля один ко многим, автоподстановка'''
        serializer.save(addedBy=self.request.user)


class PersonsDetail(RetrieveAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsListSerializer
    lookup_field = 'name'


class PersonsUpdate(RetrieveUpdateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'name'

    def perform_update(self, serializer):
        '''использует идентификатор текущего пользователя для поля один ко многим, автоподстановка'''
        serializer.save(addedBy=self.request.user)


class PersonsDelete(DestroyAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsListSerializer
    lookup_field = 'name'

# ----------------------------------------------------------------------------------------------------------------------

class SitesList(ListAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesListSerializer


class SitesCreate(CreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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