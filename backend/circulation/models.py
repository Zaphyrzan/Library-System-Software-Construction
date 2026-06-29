"""Circulation / Loan Management component."""
from datetime import timedelta
from django.db import models
from django.utils import timezone

from catalog.models import BookCopy
from members.models import Member, Staff


class Loan(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        RETURNED = "RETURNED", "Returned"
        OVERDUE = "OVERDUE", "Overdue"

    copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name="loans")
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="loans")
    staff = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name="processed_loans"
    )
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ["-loan_date"]

    def __str__(self):
        return f"Loan #{self.pk} - {self.copy}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now().date() + timedelta(
                days=self.member.membership.loan_duration_days
            )
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.status != self.Status.ACTIVE:
            return False
        return timezone.now().date() > self.due_date
