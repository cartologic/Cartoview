import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from geonode.layers.models import Layer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render

from .models import LayerAttachment
from .serializers import AttachmentSerializer, LayerSerializer
from ..app_manager.views import StandardAppViews


class LayerViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows layers to be viewed only
    """

    def get_queryset(self):
        """
        Override the default queryset to retrieve only the layers that have attachments
        """
        target_layer_ids = []
        for instance in Layer.objects.all():
            if instance.layer_attachments.all().count() > 0:
                target_layer_ids.append(instance.id)
        return Layer.objects.filter(id__in=target_layer_ids)

    serializer_class = LayerSerializer


class AttachmentFilter(django_filters.FilterSet):
    class Meta:
        model = LayerAttachment
        fields = ['id', 'layer__id', 'layer__name', 'feature_id', 'created_by__username']


class AttachmentViewSet(ModelViewSet):
    """
    API endpoint that allows collection records attachments to be viewed or edited
    """
    queryset = LayerAttachment.objects.all()
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttachmentFilter


class AttachmentManagerViews(StandardAppViews):
    """
    Standard app views add the necessary methods "add/edit/ etc..."
    """
    pass


def view(request):
    return render(request, 'attachment_manager/view.html')