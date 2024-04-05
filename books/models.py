from django.db import models
from account.models import User
# Create your models here.


class CategoryClass(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.category_name


class BookClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(CategoryClass, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='books/media/uploads', null=True, blank=True)

    def __str__(self) -> str:
        return self.title
