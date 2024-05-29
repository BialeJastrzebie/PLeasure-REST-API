from rest_framework import viewsets, mixins


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    """Base view set for user owned models"""

    def __init__(self, model, serializer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = model.objects.all()
        self.serializer_class = serializer

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return self.serializer_class
        return self.serializer_class
