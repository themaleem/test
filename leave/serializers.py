from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Request, IpAddress

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    is_admin = serializers.ReadOnlyField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "is_admin")


class RequestSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(slug_field="first_name", read_only=True)
    work_days_in_leave_period = serializers.ReadOnlyField()
    approver = serializers.SlugRelatedField(slug_field="first_name", read_only=True)

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


class RequestApproveOrDeclineSerializer(serializers.ModelSerializer):
    approver = serializers.SlugRelatedField(slug_field="first_name", read_only=True)
    partial = True

    class Meta:
        model = Request
        fields = (
            "approver",
            "approver_remark",
            "approval_date",
            "status",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "first_name",
            "is_superuser",
            "last_login",
        )


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpAddress
        fields = (
            "pk",
            "ip_address",
            "pub_date",
        )
