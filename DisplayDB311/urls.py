from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [ #patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.display, name='display'),
    url(r'^draw/$', views.draw, name='draw'),
    url(r'^table/$', views.table, name='table'),
] #)

#if settings.DEBUG is True:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
