"""
Serializers for the user API view.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    ## noqa NOTE: This method will only be called if the validation in Meta class is success.
    ## noqa NOTE: This method overrides the default behaviour of serialzier to save validated data as is.
    ## noqa NOTE: By using the custome made create_user method.
    def create(self, validated_data):
        """Create a return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        ## noqa NOTE: This function takes in the models instance to be updated and,
        ## noqa   the validated_data passed through the serializer validation for update.

        ## noqa NOTE: pop out the password from dictionary,
        password = validated_data.pop('password', None)
        ## noqa NOTE: Calls the update method from the ModelSerializer.
        user = super().update(instance, validated_data)

        ## noqa NOTE: if user specified password ie, not None
        if password:
            ## noqa NOTE: sets new password saves and returns user back.
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the uesr auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    ## noqa NOTE: validates the data passed to view.
    def validate(self, attrs):
        """Validate and authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
