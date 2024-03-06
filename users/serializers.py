from rest_framework import serializers

class AuthSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    auth_token= serializers.CharField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()

class UserSerializer(serializers.Serializer):
    """
    Serializer the User Model
    Args:
        - serializer
    """
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()


class CohortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    year = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    author = UserSerializer(many=True)

class CohortMemberSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    member = UserSerializer(many=False)
    is_active = serializers.BooleanField()
    author = UserSerializer(many=False)