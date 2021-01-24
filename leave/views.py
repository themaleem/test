from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from .models import Request
from .serializers import RequestSerializer, RequestApproveOrDeclineSerializer


@api_view(["GET"])
def api_root(request):
    path = {}
    return Response(path)


@api_view(["GET", "POST"])
def leave_list(request):
    if request.method == "GET":
        leaves = Request.objects.filter(employee=request.user)
        serializer = RequestSerializer(leaves, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def leave_detail(request, pk):
    try:
        leave = Request.objects.get(pk=pk)
    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = RequestSerializer(leave)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = RequestSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


##view to get all pending Request requests can only be viewed by admins
@api_view(["GET"])
@permission_classes([IsAdminUser])
def pending_leaves(request):
    data = Request.objects.filter(status="pending")
    serializer = RequestSerializer(data, context={"request": request}, many=True)
    return Response(serializer.data)


# view to accept a certain users leave request can only be accessed by admins
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def approve_leave(request, pk):
    try:
        leave = Request.objects.get(pk=pk)
        if leave.status not in ["pending", "declined"]:
            return Response({"data": "Request already approved"})

    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RequestApproveOrDeclineSerializer(leave, data=request.data)
    if serializer.is_valid():
        serializer.save(approver=request.user, approval_date=datetime.now())
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view to accept a certain users leave request can only be accessed by admins
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def decline_leave(request, pk):
    try:
        leave = Request.objects.get(pk=pk)
        if leave.status not in ["approved", "pending"]:
            return Response({"data": "Request already declined"})

    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RequestApproveOrDeclineSerializer(leave, data=request.data)

    if serializer.is_valid():
        serializer.save(approver=request.user, approval_date=datetime.now())
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
