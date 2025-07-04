from django.urls import path
from .views import UserMeView, LanguageListView, DownloadHistoryView, ChangePasswordView

urlpatterns = [
    path("me/", UserMeView.as_view(), name="user-me"),
    path("languages/", LanguageListView.as_view(), name ="user-language-list"),
    path("download-history/", DownloadHistoryView.as_view(), name="user-download-history"),
    path("change-password/", ChangePasswordView.as_view(), name="user-change-password"),
]
