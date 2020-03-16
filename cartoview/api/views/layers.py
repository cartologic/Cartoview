from cartoview.connections.utils import urljoin
from cartoview.geonode_oauth.utils import geonode_oauth_utils
from cartoview.layers.models import Layer
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from ..filters import DjangoObjectPermissionsFilter, LayerFilter
from ..serializers.layers import LayerSerializer


def build_describe_feature_type(layer):
    params = {'service': 'wfs',
              'version': '2.0.0',
              'request': 'DescribeFeatureType',
              'typeNames': layer.name,
              'outputFormat': 'application/json'}
    handler = layer.server.handler
    session = handler.session
    req = session.get(layer.server.url, params=params)
    return req


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all().distinct()
    serializer_class = LayerSerializer
    filterset_class = LayerFilter
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoObjectPermissionsFilter,
                       DjangoFilterBackend, OrderingFilter, SearchFilter)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_name='attributes')
    def attributes(self, request, pk=None):
        try:
            obj = Layer.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            raise NotFound(str(e))
        layer_type = obj.server.server_type
        if layer_type == "OGC-WFS":
            try:
                response = build_describe_feature_type(obj)
                data = response.json()
                featureTypes = data.get('featureTypes')
                featureTypes = list(filter(lambda d: d.get('typeName') ==
                                           obj.name.split(":")[1], featureTypes))
                if len(featureTypes) > 0:
                    return Response(featureTypes[0], status=200)
            except BaseException as e:
                return Response({'details': str(e)}, status=500)
        return Response({}, status=200)

    @action(detail=False, methods=['get'], url_name='geonode_layers')
    def geonode_layers(self, request):
        url = getattr(settings, 'OAUTH_SERVER_BASEURL')
        url = urljoin(url, 'api', 'layers')
        u = request.user
        params = dict(request.GET)
        params.pop('format', None)
        session = geonode_oauth_utils.get_requests_session(u)
        resp = session.get(url, params=params)
        try:
            data = resp.json()
        except BaseException:
            data = resp.content
        return Response(data, status=resp.status_code)