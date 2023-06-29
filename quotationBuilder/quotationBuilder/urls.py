"""
URL configuration for quotationBuilder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.schemas import get_schema_view

from quotationBuilder.custom.mixins_routers import DefaultRouter
from quotation import views as quotation_views
from quotation.urls import router as router_quotation

from quotationBuilder import __version__


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace='rest_framework')),
    path('', include('quotation.urls')),
    # # path('', quotation_views.index, name='index'),
    # path('quotation/', include('quotation.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






#### rest API ####

default_router = DefaultRouter()
default_router.extend(router_quotation)

# to order by name in API root
default_router.registry.sort(key=lambda x: x[0])

urlpatterns_api = [
    path(
        settings.BASE_URL + 'api/schema/', get_schema_view(
            title='GW back-end system',
            description='API',
            version=__version__
        ),
        name='quotationBuilder_schema'
    ),
    path(settings.BASE_URL + 'api/', include(default_router.urls)),

    # just to be able to login to the browsable api
    path(settings.BASE_URL + 'api/auth/', include('rest_framework.urls')),

    # retrieve token with verified email check, works with allauth
    # path(settings.BASE_URL + 'api/rest/', include('dj_rest_auth.urls')),

    # registration still somewhat customised
    # path(settings.BASE_URL + 'api/rest/registration/', include('dj_rest_auth.registration.urls')),  # register through API without CSRF problems
    # re_path(rf'^{settings.BASE_URL}api/rest/registration/$', RegisterView.as_view(), name='rest_register'),
    # re_path(rf'^{settings.BASE_URL}api/rest/registration/verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
    # re_path(rf'^{settings.BASE_URL}api/rest/registration/account-confirm-email/(?P<key>.+)/$', allauth_views.confirm_email,
    #         name='account_confirm_email'),
    # re_path(r'confirm-email/(?P<key>.+)/',  name='account_confirm_email'),  # !!TODO!! how to get the BASE_URL in re_path?
]
urlpatterns += urlpatterns_api