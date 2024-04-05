from django.db import models
from account.models import AccountModel
from books.models import BookClass
# Create your models here.


class BorrowingClass(models.Model):
    account = models.ForeignKey(AccountModel, related_name='borrow', on_delete=models.CASCADE)
    book = models.ForeignKey(BookClass, related_name='books', on_delete=models.CASCADE, null=True, blank=True)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    balance_after_borrowing = models.DecimalField(decimal_places=2, max_digits=12)

    class Meta:
        ordering = ['borrowing_date']
