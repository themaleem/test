from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Request

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")


class RequestSerializer(serializers.ModelSerializer):
    # employee = serializers.SlugRelatedField(
    #     queryset=User.objects.all(), slug_field="get_full_name"
    # )
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
