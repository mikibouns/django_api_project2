from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views

router = DefaultRouter()
router.register(r'users', views.UsersViewSet, base_name='user')
router.register(r'sites', views.SitesViewSet, base_name='site')
router.register(r'persons', views.PersonsViewSet, base_name='person')
router.register(r'rank', views.PersonsPageRankViewSet, base_name='ppr')
router.register(r'keywords', views.KeyWordsViewSet, base_name='keywords')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
]
