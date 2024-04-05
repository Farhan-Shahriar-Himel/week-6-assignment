from django.db import models
from books.models import BookClass
# Create your models here.

class ReviewModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    book = models.ForeignKey(BookClass, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return f"Reviewed by {self.name}"
    