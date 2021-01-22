from django.contrib import admin

from .models import User, Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = [
        "employee_fullname",
        "start_date",
        "end_date",
        "submission_date",
        "requestor_remark",
        "approver_fullname",
        "approver_remark",
        "approval_date",
        "leave_type",
        "status",
    ]
    search_fields = [
        "user_fullname",
    ]
    list_filter = [
        "status",
    ]
