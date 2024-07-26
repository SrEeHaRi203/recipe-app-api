"""
Views for the recipe APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    #NOTE: Configurations for class, queryset --> to specify the model to be managed.
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    #NOTE: Inorder to access any enpoint in this class need to be tokenauthenticated and needs to be authenticated as well
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #NOTE: override queryset to get only the items of user.
    def get_queryset(self):
        """Retrive recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')



