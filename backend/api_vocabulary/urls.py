from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserVocabularyWordViewSet, LanguageViewSet, GenerateAudioView, BulkUploadView, BulkUploadTemplateView

router = DefaultRouter()
router.register(r'vocabulary', UserVocabularyWordViewSet, basename="vocabulary")
router.register(r'languages', LanguageViewSet, basename="language")

urlpatterns = [
    path('', include(router.urls)),
    path('generate-audio/', GenerateAudioView.as_view(), name='generate-audio'),
    path('bulk-upload-vocabulary/', BulkUploadView.as_view(), name='bulk-upload'),
    path('bulk-upload-template/', BulkUploadTemplateView.as_view(), name='bulk-upload-template'),
]
