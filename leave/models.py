import uuid
from datetime import timedelta, date

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Request(models.Model):
    STATUS = (
        ("pending", "pending"),
        ("approved", "approved"),
        ("declined", "declined"),
    )

    TYPE = (
        ("sick", "sick"),
        ("casual", "casual"),
        ("annual", "annual"),
    )

    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests"
    )
    requestor_remark = models.TextField()
    approver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="approvals",
    )
    approver_remark = models.TextField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    leave_type = models.TextField(max_length=8, choices=TYPE, default="annual")
    status = models.TextField(max_length=8, choices=STATUS, default="pending")

    def __str__(self):
        return f"E:{self.employee.get_full_name()} - Leave ID: {self.pk}"

    class Meta:
        verbose_name_plural = "Leave Requests"

    @property
    def employee_fullname(self):
        return self.employee.get_full_name()

    @property
    def approver_fullname(self):
        if not self.approver:
            return "None yet"
        return self.approver.get_full_name()

    @property
    def work_days_in_leave_period(self):
        date_count = self.start_date
        work_days = 0
        while date_count <= self.end_date:
            # 0 - 5 are work days
            if date_count.weekday() < 5:
                work_days += 1
            date_count += timedelta(days=1)
        return work_days


class IpAddress(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.ip_address}"

    class Meta:
        verbose_name_plural = "IP addresses"
