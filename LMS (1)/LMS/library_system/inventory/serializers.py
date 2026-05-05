from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='_id')
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=200)
    isbn = serializers.CharField(max_length=20)
    count = serializers.IntegerField(default=1)
    available = serializers.BooleanField(default=True)