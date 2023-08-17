from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from auth_app.views import AuthorizationPhoneView, VerifyCodeView, InputInviteCodeView

schema_view = get_schema_view(
   openapi.Info(
      title="Auth API",
      default_version='v1',
      description="Project Description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="aisaev-68@yandex.ru"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



urlpatterns =[
    path('admin/', admin.site.urls),
    path('api/', include('auth_app.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', RedirectView.as_view(url='/authorize/', permanent=True)),
    path('authorize/', AuthorizationPhoneView.as_view(), name='authorize_phone'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('input_invite_code/', InputInviteCodeView.as_view(), name='input_invite_code'),
    path('profile/', InputInviteCodeView.as_view(), name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
