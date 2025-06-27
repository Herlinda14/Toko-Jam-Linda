from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mysite.views import *
from mysite.authentication import login_view, logout, registrasi

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from artikel.views import ArtikelViewSet



router = DefaultRouter()
router.register('artikel', ArtikelViewSet, basename='artikel')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name="welcome"),
    path('artikel/<int:id>/', detail_artikel, name="detail_artikel"),
    path('artikel-not-found/', not_found_artikel, name="not_found_artikel"),
    path('toko/', toko, name="toko"),
    path('kontak/', kontak, name="kontak"),

    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/artikel_list', artikel_list, name="artikel_list"),


     path('dashboard/', include("artikel.urls")),
     path('', include('artikel.urls')),
     

     



#################API###################
   
     path('api/', include(router.urls)),



    ########### Authentication ##############
    path('auth-login', login_view, name="auth-login"),
    path('auth-logout', logout, name="logout"),
    path('auth-registrasi', registrasi, name="registrasi"),

]

# Untuk development: serve static dan media files

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)