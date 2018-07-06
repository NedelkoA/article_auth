from django.apps import AppConfig
from .signals.handlers import define_company_groups, create_profile


class ArticlesConfig(AppConfig):
    name = 'articles'
    verbose_name = 'Articles apps'

    def ready(self):
        from django.db.models.signals import post_migrate, post_save
        from django.contrib.auth.models import User
        post_migrate.connect(define_company_groups, sender=self)
        post_save.connect(create_profile, sender=User)
