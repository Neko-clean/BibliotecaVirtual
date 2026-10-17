from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField


class Libro(Document):

    titulo = StringField(
        required=True,
        max_length=200
    )

    autor = StringField(
        required=True,
        max_length=100
    )

    anio = IntField()

    meta = {
        'collection': 'libros'
    }


from django.db import models
from django.contrib.auth.models import User


class PasswordResetCode(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    code = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    used = models.BooleanField(
        default=False
    )


    def __str__(self):

        return self.user.username + " - " + self.code