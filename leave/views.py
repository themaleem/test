from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from .models import Request
from .serializers import RequestSerializer


@api_view(["GET"])
def api_root(request):
    path = {}
    # serializer = RequestSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    return Response(path)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for creating or submitting leave requests... open to anybody
@api_view(["POST"])
def create_leave(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##view to get all pending Request requests can only be viewed by admins
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_all_pending_leaves(request):
    data = Request.objects.filter(status="pending")
    serializer = RequestSerializer(data, context={"request": request}, many=True)
    return Response(serializer.data)


# view to gel all accepted leaves can only be viewed by admins
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_all_accepted_leaves(request):
    data = Request.objects.filter(state="approved")
    serializer = RequestSerializer(data, context={"request": request}, many=True)
    return Response(serializer.data)


# view to accept a certain users leave request can only be accessed by admins
@api_view(["GET"])
@permission_classes([IsAdminUser])
def leave_accept(request, pk):
    try:
        leave = Request.objects.get(pk=pk)
        if leave.status not in ["pending", "decline"]:
            return Response({"data": "Request already approved"})

    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    leave.status = "approved"
    leave.save()
    serializer = RequestSerializer(leave)
    print(serializer)
    return Response(serializer.data)


# view to accept a certain users leave request can only be accessed by admins
@api_view(["GET"])
@permission_classes([IsAdminUser])
def leave_decline(request, pk):
    try:
        leave = Request.objects.get(pk=pk)
        if leave.status not in ["approved", "pending"]:
            return Response({"data": "Request already declined"})

    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    leave.status = "decline"
    leave.save()
    serializer = RequestSerializer(leave)
    print(serializer)
    return Response(serializer.data)
