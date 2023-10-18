from django.utils import timezone
from rest_framework import serializers

from borrowings_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ["borrow_date", "user"]


class CreateBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("expected_return_date", "book")

    def validate(self, data):
        book = data["book"]
        if book.inventory == 0:
            raise serializers.ValidationError("The book is out of stock.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)


class UpdateBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("expected_return_date", "actual_return_date")

    def validate(self, data):
        actual_return_date = data.get("actual_return_date")
        borrow_date = data.get("borrow_date")

        if actual_return_date and actual_return_date > timezone.now().date():
            raise serializers.ValidationError("The actual return date cannot be in the future.")

        if borrow_date and actual_return_date and actual_return_date < borrow_date:
            raise serializers.ValidationError("The actual return date cannot be before the borrow date.")

        return data
