"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from dummygenerator.views import (
    HomepageView,
    Login,
    Logout,
    SignupView,
    Profile,
    HomeRedirect,
    ListSchemas,
    CreateSchema,
    EditSchema,
    DeleteSchema,
    ListDataSets,
)

urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    # TODO: REWRITE FOR NAMESPACES
    path("schemas/", ListSchemas.as_view(), name="list"),
    path("schemas/create", CreateSchema.as_view(), name="create"),
    path("schemas/edit/<pk>", EditSchema.as_view(), name="edit"),
    path("schemas/delete/<pk>", DeleteSchema.as_view(), name="delete"),
    path("schemas/export/<pk>", ListDataSets.as_view(), name="datasets"),
    path("accounts/login/", Login.as_view(), name="login"),
    path("accounts/logout/", Logout.as_view(), name="logout"),
    path("accounts/signup/", SignupView.as_view(), name="signup"),
    path("accounts/profile/", Profile.as_view(), name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", HomeRedirect.as_view()),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


if settings.HEROKU_MEDIA:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
