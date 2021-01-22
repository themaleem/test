from rest_framework import serializers
from .models import Employee, Request

# class UserSerializer(serializers.ModelSerializer):


class RequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Request
        fields = (
            "url",
            "pk",
            "start_date",
            "end_date",
            "submission_date",
            "employee",
            "requestor_remark",
            "approver",
            "approver_remark",
            "approval_date",
            "leave_type",
            "status",
        )


class UserRequestSerializer(serializers.HyperlinkedModelSerializer):
    requests = RequestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "url",
            "pk",
            "full_name",
            "email",
            "is_superuser",
            "last_login",
            "requests",
        )
