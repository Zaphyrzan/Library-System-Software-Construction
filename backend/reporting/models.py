"""Reporting & Fine Management component: fines and notifications."""
from django.db import models

from circulation.models import Loan
from members.models import Member


class Fine(models.Model):
    class Reason(models.TextChoices):
        OVERDUE = "OVERDUE", "Overdue"
        DAMAGE = "DAMAGE", "Damage"
        LOST = "LOST", "Lost"

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="fines")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    reason = models.CharField(max_length=20, choices=Reason.choices, default=Reason.OVERDUE)
    issued_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Fine RM{self.amount} ({self.reason})"


class Notification(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=300)
    sent_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_date"]

    def __str__(self):
        return f"To {self.member.name}: {self.message[:40]}"
