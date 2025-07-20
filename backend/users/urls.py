from django.urls import path
from .views import UserMeView, LanguageListView, DownloadHistoryView, ChangePasswordView, DeleteAccountView, RegisterUserView, VerifyEmailView

urlpatterns = [
    path("me/", UserMeView.as_view(), name="user-me"),
    path("languages/", LanguageListView.as_view(), name ="user-language-list"),
    path("download-history/", DownloadHistoryView.as_view(), name="user-download-history"),
    path("change-password/", ChangePasswordView.as_view(), name="user-change-password"),
    path("me/delete/", DeleteAccountView.as_view(), name="user-delete-account"),
    path("register/", RegisterUserView.as_view(), name="user-register"),
    path("verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
]