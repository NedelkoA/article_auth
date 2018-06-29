from django.db import models


class Category(models.Model):
    name_category = models.CharField(max_length=64)

    def __str__(self):
        return self.name_category
    

class Article(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField()
    status = models.CharField(max_length=10, default='REVIEW')
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
