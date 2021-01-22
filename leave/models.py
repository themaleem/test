import uuid
from datetime import timedelta, date

from django.db import models
from django.contrib.auth.models import User


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
