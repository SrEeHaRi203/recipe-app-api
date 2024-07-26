"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
    )


## noqa NOTE: The generics.CreateAPIView can handle http POST requests that is designed to create objects in  DB.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    ## noqa NOTE: set the serializer_class on this view.
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    ## noqa NOTE: use the ObtainAuthToken class behaviour and maeke it use our serializer(AuthTokenSerializer)
    ## noqa Overriding the class as we use username as email rather than the default username.
    serializer_class = AuthTokenSerializer
    ## noqa NOTE: (optional) uses the default rendered class for ObtainAuthToken,
    ## noqa to show in the UI, as overriding the serializer will not include it by default
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    ## noqa NOTE:RetrieveUpdateAPIView for retrieving and updating obj in the database.
    ## noqa NOTE:user modified UserSerializer.
    serializer_class = UserSerializer
    ## noqa NOTE: To get the authentication and permissions for using this API.
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    ## noqa NOTE: get_object is overrided, get_objects gets the objects for http get request or any request for this API.
    ## noqa NOTE: Here overrides to get the
    def get_object(self):
        """Retrieve and return the authenticated User."""
        return self.request.user
