from rest_framework import pagination, serializers

class CurrentPageField(serializers.Field):
    def to_representation(self, value):
        return value.number

class PagSerializer(serializers.Serializer):
    page = CurrentPageField(source='*')
    pages = serializers.ReadOnlyField(source='paginator.num_pages')
    per_page = serializers.ReadOnlyField(source='paginator.per_page')
    total = serializers.ReadOnlyField(source='paginator.count')

class CybPaginationSerializer(pagination.BasePaginationSerializer):
    pagination = PagSerializer(source='*')
