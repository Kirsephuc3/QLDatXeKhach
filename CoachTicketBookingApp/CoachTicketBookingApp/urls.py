from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CoachTicket App API",
        default_version='v1',
        description="APIs for CoachTicketApp",
        contact=openapi.Contact(email="2151010290phuc@ou.edu.vn"),
        license=openapi.License(name="Đặng Minh Phúc@2024"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('', include('CoachTicketBooking.urls')),
    path('admin/', admin.site.urls),

    # SWAGGER
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # CKEDITOR
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('o/', include('oauth2_provider.urls',
                       namespace='oauth2_provider')),

]