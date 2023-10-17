from django.urls import include, path
from rest_framework import routers

from borrowings_service.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowings/user_borrowings/",
        BorrowingViewSet.as_view({"get": "user_borrowings"}),
        name="user-borrowings"
    ),
]

app_name = "borrowings_service"
