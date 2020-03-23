from rest_framework import serializers
from django.contrib.auth import password_validation
from . import models


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for change password"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = models.UserProfile
        fields = ['old_password', 'new_password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer to update user object"""

    class Meta:
        model = models.UserProfile
        fields = ['id', 'name', 'phone']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ['id', 'email', 'name', 'phone', 'user_type', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'user_type': {
                'style': {
                    'placeholder': "Customer / Service Provider"
                }
            }
        }

    def validate_password(self, password):
        """Validate Password"""
        password_validation.validate_password(password, self.instance)
        return password

    def validate(self, data):
        """Validate phone field"""
        if not data['phone'].isnumeric():
            raise serializers.ValidationError("Please enter a valid phone number.")
        elif len(data['phone']) != 10:
            raise serializers.ValidationError("Ensure phone length is of 10 digits.")
        elif data['user_type'] not in ('Consumer', 'Service Provider'):
            raise serializers.ValidationError("Ensure user type is only either a 'consumer' or a 'service provider'.")
        else:
            return data

    def create(self, validated_data):
        """Create and return new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            phone=validated_data['phone']
        )
        return user


class ServiceSerializer(serializers.ModelSerializer):
    """Create a new service"""
    service_provider_name = serializers.SerializerMethodField('get_provider_name')

    class Meta:
        model = models.Service
        fields = ('id', 'service_name', 'service_desc', 'service_provider_id', 'service_provider_name')
        extra_kwargs = {
            'id': {'read_only': True},
            'service_provider_id': {'read_only': True},
            'service_provider_name': {'read_only': True}
        }

    def get_provider_name(self, data):
        return data.service_provider.name


class RequestSerializer(serializers.ModelSerializer):
    """Create a new request"""
    provider_name = serializers.SerializerMethodField('get_service_provider_name')
    service_name = serializers.SerializerMethodField('get_services_name')

    class Meta:
        model = models.RequestService

        fields = ('id', 'consumer', 'provider_name', 'service_id', 'service_name', 'request_desc',
                  'status', 'comments')

        extra_kwargs = {
            'id': {'read_only': True},
            'consumer': {
                'read_only': True
            },
            'service_name': {
                'read_only': True
            },
            'provider_name': {
                'read_only': True
            },
            'comments': {
                'read_only': True
            },
        }

    def get_service_provider_name(self, data):
        return data.service_id.service_provider.name

    def get_services_name(self, data):
        return data.service_id.service_name


class CommentSerializer(serializers.ModelSerializer):
    """Create a new comment"""
    author_name = serializers.SerializerMethodField('get_authors_name')

    class Meta:
        model = models.Comment
        fields = ('id', 'request', 'author', 'content', 'author_name')
        extra_kwargs = {
            'author': {
                'read_only': True
            },
            'author_name': {
                'read_only': True
            }
        }

    def get_authors_name(self, data):
        return data.author.name


    def get_service_name(selfSelf,data):
        return data.service_name
