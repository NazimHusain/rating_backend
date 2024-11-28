from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.users import models as UserModels
from apps.recipes import models as RecipeModels
from apps.recipes import serializers as RecipeSerializers
from django.shortcuts import get_object_or_404
from django.db.models import Avg


class RecipeListCreateAPIView(APIView):
    permission_classes = [UserModels.IsSeller]

    def get(self, request, version):
        recipes = RecipeModels.Recipe.objects.all()
        serializer = RecipeSerializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, version):
        seller = request.user
        request.data["seller"] = seller.id
        serializer = RecipeSerializers.RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,version, pk):
        recipe = get_object_or_404(RecipeModels.Recipe, id=pk, is_deleted=False)
        serializer = RecipeSerializers.RecipeSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, version,pk):
        recipe = get_object_or_404(RecipeModels.Recipe, id=pk, is_deleted=False)
        recipe.delete()
        return Response({'message': 'Recipe deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    
class RecipeDetailAPIView(APIView):
    permission_classes = [UserModels.IsCustomer]

    def get(self, request,version, pk=None):
        if pk:
            recipe = get_object_or_404(RecipeModels.Recipe, id=pk, is_deleted=False)
            serializer = RecipeSerializers.RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        recipes = RecipeModels.Recipe.objects.all()
        serializer = RecipeSerializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

  

class RecipeRatingAPIView(APIView):
    permission_classes = [UserModels.IsCustomer]
    
    def post(self, request, version):
        customer = request.user
        request.data["customer"] = customer.id
        serializer = RecipeSerializers.RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  
    def get(self, request, version, recipe_id):
        recipe = get_object_or_404(RecipeModels.Recipe, id=recipe_id, is_deleted=False)
        recipe_serializer = RecipeSerializers.RecipeSerializer(recipe)
        ratings = recipe.ratings.all()
        ratings_serializer = RecipeSerializers.RatingSerializer(ratings, many=True)
        avg_rating = ratings.aggregate(Avg('rating')).get('rating__avg', 0) or 0
        response_data = {
            "recipe": recipe_serializer.data,
             "ratings": ratings_serializer.data,
            "average_rating": round(avg_rating, 2),
            "total_ratings": ratings.count(),
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    
