# from django.shortcuts import render
# from rest_framework import mixins, viewsets
#
# from borrowings_service.models import Borrowing
# from borrowings_service.serializers import BorrowingSerializer
#
#
# class BorrowingViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Borrowing.objects.select_related("books", "users")
#     serializer_class = BorrowingSerializer
