from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='_id')
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['admin', 'employee', 'user'], default='user')


