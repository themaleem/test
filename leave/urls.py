from django.urls import path

from . import views

app_name = "leave"

urlpatterns = [
    path("", views.api_root),
    path("leave/", views.leave_list),
    path("leave/<int:pk>/", views.leave_detail),
    path("pending-leaves/", views.pending_leaves),
    path("accept/<int:pk>/", views.approve_leave),
    path("decline/<int:pk>", views.decline_leave),
]


# urlpatterns = [
#     path("", views.api_root),
#     # path("create/", views.create_leave),
#     # path("pending", views.get_all_pending_leaves),
#     # path("accepted", views.get_all_accepted_leaves),
#     # path("declined", views.get_all_declined_leaves),
#     # path("accept/<int:pk>", views.leave_accept),
# ]
