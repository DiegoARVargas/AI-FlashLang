from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VocabularyWordViewSet, LanguageViewSet

router = DefaultRouter()
router.register(r'vocabulary', VocabularyWordViewSet, basename="vocabulary")
router.register(r'languages', LanguageViewSet, basename="language")

urlpatterns = [
    path('', include(router.urls)),
]