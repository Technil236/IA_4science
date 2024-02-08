from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "pseudonym", "avatar", "sex", "birthday"]
        error_class = "error"

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ["email", "pseudonym", "avatar", "sex", "birthday"]
        error_class = "error"

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "pseudonym", "avatar", "sex", "birthday"]
