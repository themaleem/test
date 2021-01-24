from django.urls import path

from . import views

app_name = "leave"

urlpatterns = [
    path("", views.api_root),
    path("auth/users/mee", views.mee),
    path("leave/", views.leave_list),
    path("leave/<int:pk>/", views.leave_detail),
    path("admin-leaves/", views.admin_leaves),
    path("approve/<int:pk>/", views.approve_leave),
    path("decline/<int:pk>/", views.decline_leave),
    path("all-ips/", views.all_ips),
]
