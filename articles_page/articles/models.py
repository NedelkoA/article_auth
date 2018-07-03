from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from .signals.handlers import my_handler


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name_category


class CustomUser(User):
    telephone = models.CharField(max_length=13, blank=True, validators=[
        RegexValidator('^\+380\d{9}$',
                       'Phone number must be entered in the format: \'+380xxxxxxxxx\'.')
    ])

    def __str__(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=20, unique=True)
    text = models.TextField()
    status = models.CharField(max_length=10, default='REVIEW')
    user = models.ForeignKey(
        User,
        models.PROTECT,
        related_name='articles',
        null=True
    )
    category = models.ForeignKey(
        Category,
        models.PROTECT,
        related_name='articles'
    )

    class Meta:
        permissions = (
            ('change_status', 'Can change status'),
        )

    def __str__(self):
        return self.title


post_save.connect(my_handler, sender=User)
