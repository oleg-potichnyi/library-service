from django.urls import include, path
from rest_framework import routers

from borrowings_service.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowings/<int:pk>/return/",
        BorrowingViewSet.as_view({"post": "return_book"}),
        name="borrowing-return"
    ),
]

app_name = "borrowings_service"
