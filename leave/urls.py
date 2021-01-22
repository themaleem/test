from django.urls import path

from . import views

app_name = "leave"

urlpatterns = [
    path("", views.api_root),
    path("create/", views.create_leave),
    path("pending", views.get_all_pending_leaves),
    path("accept/<int:pk>", views.leave_accept),
    path("accepted", views.get_all_accepted_leaves),
]
