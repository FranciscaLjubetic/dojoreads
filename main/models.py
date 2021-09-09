from django.db import models
import re
from datetime import date, datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 2:
            errors['firstname_len'] = "nombre debe tener al menos 2 caracteres de largo";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombreporfavor"

        if len(postData['password']) < 4:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors
    
    

class Books_manager(models.Manager):
    def basic_validator(self, post_data):
        errors ={}
        #today = date.today()
        
        if len(post_data['title'])<2:
            errors['title'] = 'The title should have at least 2 characters'
        
        return errors


class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length= 100)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.URLField(
        default='https://www.pngkey.com/png/full/331-3315307_our-insert-name-here-meme.png')
    role = models.CharField(max_length=255, choices=CHOICES, default='user')
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
    


class Author(models.Model):
    name = models.CharField(max_length=255, unique= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Books(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, related_name="books", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Books_manager()
    


class Reviews(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="review", on_delete = models.CASCADE)
    book = models.ForeignKey(Books, related_name="review", on_delete = models.CASCADE)

    
    




