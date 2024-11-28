from rest_framework import serializers
from .models import Recipe, Rating

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'seller', 'name', 'description', 'image']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'customer', 'recipe', 'rating']
