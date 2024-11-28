from django.db import models
from apps.helpers import models as coreModels

class Recipe(coreModels.AbstractDateTimeModel):
    seller = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ForeignKey(
        coreModels.FileUpload,
        null=True,
        blank=True,
        related_name="recipes",
        on_delete=models.PROTECT,
    )
    

class Rating(coreModels.AbstractDateTimeModel):
    customer = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='ratings')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()  
    
    class Meta:
        unique_together = ('customer', 'recipe') 

    def __str__(self):
        return f"{self.customer.username} - {self.recipe.name} ({self.rating})"





