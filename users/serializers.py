"""
Serializer
"""
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        """
        Set fields
        """
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }
        fields = (
            'id',
            'date_joined',
            'last_login',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'password',
        )

    def create(self, validated_data):
        """
        Set Password
        """
        user = super(UserSerializer, self).create(validated_data)
        user.username = user.email
        user.set_password(user.password)
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        If a password on the data request then set password,
        and also if an email the data request then set username as an email
        """
        user = super(UserSerializer, self).update(instance, validated_data)

        password = validated_data.get('password', None)
        if password:
            user.is_user_password = True
            user.set_password(user.password)

        email = validated_data.get('email', None)
        if email:
            user.username = email

        if password or email:
            user.save()

        return user
