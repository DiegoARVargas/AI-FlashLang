from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_premium = models.BooleanField(default=False)  # Indica si el usuario tiene una cuenta premium
    preferred_language = models.CharField(
        max_length=10,
        choices=[("es", "Español"), ("en", "Inglés"), ("fr", "Francés")],
        default="es",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username