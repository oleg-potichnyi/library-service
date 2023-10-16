from rest_framework import serializers

from books_service.models import Book


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "is_active",
            "book",
            "user",
        )
