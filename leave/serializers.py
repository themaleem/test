from rest_framework import serializers
from .models import User, Request

# class UserSerializer(serializers.ModelSerializer):


class RequestSerializer(serializers.ModelSerializer):
    work_days_in_leave_period = serializers.ReadOnlyField()

    class Meta:
        model = Request
        fields = (
            # "url",
            "pk",
            "start_date",
            "end_date",
            "work_days_in_leave_period",
            "submission_date",
            "employee",
            "requestor_remark",
            "approver",
            "approver_remark",
            "approval_date",
            "leave_type",
            "status",
        )


class UserRequestSerializer(serializers.ModelSerializer):
    requests = RequestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            # "url",
            "pk",
            "full_name",
            "email",
            "is_superuser",
            "last_login",
            "requests",
        )
