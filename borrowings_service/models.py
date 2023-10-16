# from django.db import models
#
# from books_service.models import Book
# from users_service.models import User
#
#
# class Borrowing(models.Model):
#     borrow_date = models.DateField()
#     expected_return_date = models.DateField()
#     actual_return_date = models.DateField()
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self) -> str:
#         return f"Borrowing ID: {self.pk}"
