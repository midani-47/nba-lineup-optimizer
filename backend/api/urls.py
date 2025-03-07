from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, TeamViewSet, PlayerViewSet, 
    LineupViewSet, LineupComparisonViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'lineups', LineupViewSet, basename='lineup')
router.register(r'comparisons', LineupComparisonViewSet, basename='comparison')

urlpatterns = [
    path('', include(router.urls)),
] 