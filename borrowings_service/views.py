from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from borrowings_service.models import Borrowing
from borrowings_service.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowings_service.serializers import BorrowingSerializer, CreateBorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["is_active"]
    ordering_fields = ["expected_return_date"]

    def get_queryset(self):
        """Allow non-admin users to see their own borrowings"""
        user = self.request.user
        if not user.is_staff:
            return Borrowing.objects.filter(user=user)
        return Borrowing.objects.all()

    def create(self, request, *args, **kwargs):
        """Validate that the book's inventory is not zero"""
        book = request.data.get('book')
        if book.inventory == 0:
            raise ValidationError("The book is out of stock.")
        book.inventory -= 1
        book.save()
        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer):
        """Check this borrowing has already been returned"""
        borrowing = self.get_object()
        if not borrowing.is_active:
            raise ValidationError("This borrowing has already been returned.")
        borrowing.is_active = False
        borrowing.save()
        book = borrowing.book
        book.inventory += 1
        book.save()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return BorrowingSerializer
        return CreateBorrowingSerializer

    @action(detail=False, methods=['get'])
    def user_borrowings(self, request):
        """Filter borrowing by user ID for administrators"""
        if request.user.is_staff:
            user_id = request.query_params.get("user_id")
            if user_id:
                borrowings = Borrowing.objects.filter(user=user_id)
            else:
                borrowings = Borrowing.objects.all()
        else:
            borrowings = Borrowing.objects.filter(user=request.user)
        serializer = BorrowingSerializer(borrowings, many=True)
        return Response(serializer.data)
