"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import json
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
# from graphene_django.views import GraphQLView
# from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_file_upload.django import FileUploadGraphQLView

from rest_framework import routers

from apps.users.views import MeView
from apps.parking_lot.views import ParkedItemViewSet


class CustomGraphQLView(FileUploadGraphQLView):
    """Handles multipart/form-data content type in django views"""
    def parse_body(self, request):
        """
        Allow for variable batch
        https://github.com/graphql-python/graphene-django/issues/967#issuecomment-640480919
        :param request:
        :return:
        """
        try:
            body = request.body.decode("utf-8")
            request_json = json.loads(body)
            self.batch = isinstance(request_json, list)
        except:  # noqa: E722
            self.batch = False
        return super().parse_body(request)


CustomGraphQLView.graphiql_template = "graphene_graphiql_explorer/graphiql.html"

router = routers.DefaultRouter()
router.register(r'parking-lot', ParkedItemViewSet, basename='parking-lot')

urlpatterns = [
    path('admin', admin.site.urls),
    path('graphiql', csrf_exempt(CustomGraphQLView.as_view(graphiql=True))),
    path('graphql', csrf_exempt(CustomGraphQLView.as_view())),
    path('webhooks', include('helix.webhooks')),
    path('api/me/', MeView.as_view()),
    path('api/', include(router.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns