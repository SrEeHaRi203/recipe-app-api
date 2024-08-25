"""
Serializers for recipe APIs
"""

from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipies"""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only = ['id']

    def create(self, validated_data):
        """Create a recipe."""
        ## noqa NOTE: This removes tags data from validated_data,
        tags = validated_data.pop('tags', [])
        ## noqa NOTE: Create recipe with the remaining data.
        recipe  = Recipe.objects.create(**validated_data)
        ## noqa NOTE: context is passed form the view to the serializer
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

        return recipe

## noqa NOTE:Get all functionality and add extra fields from RecipeSerializer
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']



