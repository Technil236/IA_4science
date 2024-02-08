from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.db import models
from coolname import generate_slug
from django.core.mail import send_mail
import random

class CustomUserManager(BaseUserManager):
    
    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Vous devez fournir un email valide"))

    def create_user(self, email, pseudonym, avatar, sex, birthday, password, **extra_fields):
        if not pseudonym:
            raise ValueError(_("Les utilisateurs doivent soumettre un pseudonyme"))
        
        if not avatar:
            raise ValueError(_("Les utilisateurs doivent choisir leur avatar"))
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("L'utiisateur de base: et l'email est requis"))
        
        user = self.model(
            pseudonym=pseudonym,
            # avatar=avatar,
            email=email,
            sex=sex,
            birthday=birthday,
            **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        user.save()
        
        return user

    def create_superuser(self, email, pseudonym, avatar, sex, birthday, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers must have is_staff=True"))
        
        if not password:
            raise ValueError(_("Superusers must have a password"))
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("L'administrateur de base: et l'email est requis"))
        
        avatar_instance = Avatar.objects.get(id=1)

        
        user = self.create_user(email, pseudonym, avatar_instance, sex, birthday, password, **extra_fields)
        
        return user

def generate_pseudonym():
    pseudonym = ' '.join(random.choices([generate_slug(3), generate_slug(2)]))
    return pseudonym.capitalize()

class Avatar(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.URLField()
    
    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    
    SEX_CHOICES = (
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    )
    
    pseudonym = models.CharField(_("Pseudonyme"), max_length=250, default=generate_pseudonym, unique=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True)
    sex = models.CharField(max_length=32, choices=SEX_CHOICES)
    birthday = models.DateField('date de naissance', default='2000-01-01')
    email = models.EmailField(_("Adresse mail"), max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["pseudonym", "avatar", "sex", "birthday"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        
    def __str__(self):
        return self.pseudonym
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

def get_absolute_url(self):
        return "/accounts/%i/" % (self.pk)