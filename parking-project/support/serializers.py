from rest_framework import serializers

from support.models import Support


class SupportSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='user.role', required=False, read_only=True)
    firstName = serializers.CharField(source='user.firstName', required=False)
    lastName = serializers.CharField(source='user.lastName', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    profilePhoto = serializers.ImageField(source='user.profilePhoto', required=False)

    class Meta:
        model = Support
        fields = ['id', 'role', 'firstName', 'lastName', 'email', 'profilePhoto']
