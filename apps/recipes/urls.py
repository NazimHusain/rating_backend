from django.urls import path
from apps.recipes.views import RecipeListCreateAPIView,RecipeDetailAPIView, RecipeRatingAPIView

urlpatterns = [
    path('create/', RecipeListCreateAPIView.as_view(), name='recipe-list-create'),
    path('create/<int:pk>/', RecipeListCreateAPIView.as_view(), name='recipe-list-create'),
    path('recipe/<int:pk>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
    path('recipe/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
    path('rating/', RecipeRatingAPIView.as_view(), name='rating-create'),
    path('rating/<int:recipe_id>/', RecipeRatingAPIView.as_view(), name='rating'),
]
