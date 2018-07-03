from django.conf.urls import url, include
from . import views
from rest_framework.authtoken import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'users', views.UsersViewSet, base_name='user')
# router.register(r'sites', views.SitesViewSet, base_name='site')
# router.register(r'persons', views.PersonsViewSet, base_name='person')
# router.register(r'rank', views.PersonsPageRankViewSet, base_name='ppr')
# router.register(r'keywords', views.KeyWordsViewSet, base_name='keywords')

# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-token-auth/', auth_views.obtain_auth_token),
# ]


users_lc = views.UsersViewSet.as_view({'get': 'list', 'post': 'create'})
users_rud = views.UsersViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'})
persons_lc = views.PersonsViewSet.as_view({'get': 'list', 'post': 'create'})
persons_rud = views.PersonsViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'})
persons_rank_lc = views.PersonsPageRankViewSet.as_view({'get': 'list'})
persons_rank_rud = views.PersonsPageRankViewSet.as_view({'get': 'retrieve'})
sites_lc = views.SitesViewSet.as_view({'get': 'list', 'post': 'create'})
sites_rud = views.SitesViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'})
persons_rank_date_lc = views.PPRDateViewSet.as_view({'get': 'list'})
persons_rank_date_r = views.PPRDateViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    url(r'^$', views.APIRootView.as_view(), name='api_root'),
    url(r'^api-token-auth/', auth_views.obtain_auth_token, name='token_auth'),

    url(r'^users/$', users_lc, name='users_lc'),
    url(r'^users/(?P<pk>\d+)/$', users_rud, name='users_rud'),

    url(r'^persons/rank/$', persons_rank_lc, name='ppr_lc'),
    url(r'^persons/rank/(?P<pk>\d+)/$', persons_rank_rud, name='ppr_rud'),

    url(r'^persons/rank/date/$', persons_rank_date_lc, name='ppr_date_lc'),
    url(r'^persons/rank/(?P<pk>\d+)/date/$', persons_rank_date_r, name='ppr_date_r'),

    url(r'^persons/$', persons_lc, name='persons_lc'),
    url(r'^persons/(?P<pk>\d+)/$', persons_rud, name='persons_rud'),

    url(r'^sites/$', sites_lc, name='sites_lc'),
    url(r'^sites/(?P<pk>\d+)/$', sites_rud, name='sites_rud'),
]
