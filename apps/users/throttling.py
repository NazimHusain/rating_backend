from rest_framework.throttling import UserRateThrottle

class RecipeThrottling(UserRateThrottle):
    scope = 'recipe'