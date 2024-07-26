"""URLs mapping for the recipe app"""

from django.urls import (
    path,
    include
)
# NOTE: automatically create routes,
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]