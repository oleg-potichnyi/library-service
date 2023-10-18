from django.db import models

from books_service.models import Book
from users_service.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Borrowing ID: {self.pk}"


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    class TypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT"
        FINE = "FINE"
    status = models.CharField(max_length=50, choices=StatusChoices.choices)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session = models.URLField()
    session_id = models.TextField()
    money_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment ID: {self.pk}"
