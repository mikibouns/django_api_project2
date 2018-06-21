from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^users/$', views.UsersList.as_view(), name='users_list'),
    url(r'^users/create/$', views.UsersCreate.as_view(), name='users_create'),
    url(r'^users/(?P<pk>\d+)/$', views.UsersDetail.as_view(), name='users_detail'),
    url(r'^users/(?P<pk>\d+)/edit/$', views.UsersUpdate.as_view(), name='users_update'),
    url(r'^users/(?P<pk>\d+)/delete/$', views.UsersDelete.as_view(), name='users_delete'),

    url(r'^persons/rank/$', views.PersonsPageRankList.as_view(), name='ppr_list'),
    url(r'^persons/rank/(?P<pk>\d+)/$', views.PersonsPageRankDetail.as_view(), name='ppr_detail'),
    url(r'^persons/rank/date/$', views.PersonsPageRankDateList.as_view(), name='ppr_list_date'),
    url(r'^persons/rank/(?P<pk>\d+)/date/$', views.PersonsPageRankDateDetail.as_view(), name='ppr_detail_date'),

    url(r'^persons/$', views.PersonsList.as_view(), name='persons_list'),
    url(r'^persons/create/$', views.PersonsCreate.as_view(), name='persons_create'),
    url(r'^persons/(?P<pk>\w+)/$', views.PersonsDetail.as_view(), name='persons_detail'),
    url(r'^persons/(?P<pk>\w+)/edit/$', views.PersonsUpdate.as_view(), name='persons_update'),
    url(r'^persons/(?P<pk>\w+)/delete/$', views.PersonsDelete.as_view(), name='persons_delete'),

    url(r'^sites/$', views.SitesList.as_view(), name='sites_list'),
    url(r'^sites/create/$', views.SitesCreate.as_view(), name='sites_create'),
    url(r'^sites/(?P<pk>\d+)/$', views.SitesDetail.as_view(), name='sites_detail'),
    url(r'^sites/(?P<pk>\d+)/edit/$', views.SitesUpdate.as_view(), name='sites_update'),
    url(r'^sites/(?P<pk>\d+)/delete/$', views.SitesDelete.as_view(), name='sites_delete'),
]
