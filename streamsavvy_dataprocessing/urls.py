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
from rest_framework_jwt.views import obtain_jwt_token

from data_processor.views import ServiceDescriptionViewSet, SearchContentViewSet, ChannelViewSet, ContentViewSet, \
    ViewingServicesViewSet, ModuleDescriptionViewSet

router = routers.DefaultRouter()
router.register(r'service_description', ServiceDescriptionViewSet)
router.register(r'search', SearchContentViewSet, 'search')
router.register(r'content', ContentViewSet, 'content')
router.register(r'channel', ChannelViewSet, 'channel')
router.register(r'window', ViewingServicesViewSet, 'viewingservices')
router.register(r'modules', ModuleDescriptionViewSet, 'moduledescriptions')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'api-token-auth', obtain_jwt_token)
    # url(r'haystack_search', autocomplete, name='autocomplete'),

]
