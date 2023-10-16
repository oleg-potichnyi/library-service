from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingSerializer


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("books", "users")
    serializer_class = BorrowingSerializer

    def return_book(self, request, pk=None):
        try:
            borrowing = Borrowing.objects.get(pk=pk)
        except Borrowing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        borrowing.actual_return_date = serializers.DateField(format="%Y-%m-%d").to_internal_value(
            request.data.get("actual_return_date"))
        borrowing.is_active = False
        borrowing.save()
        return Response(BorrowingSerializer(borrowing).data)
