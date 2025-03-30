from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VocabularyWordViewSet

router = DefaultRouter()
router.register(r'vocabulary', VocabularyWordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]