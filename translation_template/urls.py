from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/', include('app.api.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
)
