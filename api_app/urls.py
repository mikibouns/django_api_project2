from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', views.UsersViewSet, base_name='user')
router.register(r'sites', views.SitesViewSet, base_name='site')
router.register(r'persons', views.PersonsViewSet, base_name='person')
router.register(r'rank', views.PersonsPageRankViewSet, base_name='ppr')


urlpatterns = [
    url(r'^', include(router.urls)),
]
