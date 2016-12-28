"""streamsavvy_dataprocessing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from data_processor.views import *

router = routers.DefaultRouter()
router.register(r'popular-shows', PopularShowsViewSet, 'popular_shows')
router.register(r'service_description', ServiceDescriptionViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'search', SearchContentViewSet, 'search')
router.register(r'search_sports', SearchSportsViewSet, 'sport')
router.register(r'content', ContentViewSet, 'content')
router.register(r'channel', ChannelViewSet, 'channel')
router.register(r'window', ViewingServicesViewSet, 'viewingservices')
router.register(r'modules', ModuleDescriptionViewSet, 'moduledescriptions')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    # url(r'^sport_schedule/(?P<sport_id>\d+)', SportScheduleView.as_view(), name='sport_schedule'),
    # url(r'^api/guide/(?P<lat>\d{1,2}\.\d{1,20})/(?P<long>-?\d{1,3}\.\d{1,20})', RoviChannelGridView.as_view(),
    #     name='rovi_channel_grid_view'),

    # url(r'haystack_search', autocomplete, name='autocomplete'),

]
