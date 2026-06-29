"""Member Management component: members, membership rules, staff."""
from django.contrib.auth.models import User
from django.db import models


class Membership(models.Model):
    """Data-driven borrowing rules, shared by many members."""
    type_name = models.CharField(max_length=50, unique=True)
    loan_limit = models.PositiveIntegerField(default=3)
    loan_duration_days = models.PositiveIntegerField(default=14)
    can_reserve = models.BooleanField(default=True)

    def __str__(self):
        return self.type_name


class Member(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        EXPIRED = "EXPIRED", "Expired"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="member"
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT, related_name="members")
    membership_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def active_loan_count(self):
        # "ACTIVE" matches circulation.Loan.Status.ACTIVE
        return self.loans.filter(status="ACTIVE").count()

    @property
    def can_borrow(self):
        return self.status == self.Status.ACTIVE and self.active_loan_count < self.membership.loan_limit


class Staff(models.Model):
    class Role(models.TextChoices):
        LIBRARIAN = "LIBRARIAN", "Librarian"
        ADMIN = "ADMIN", "Administrator"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff")
    name = models.CharField(max_length=200)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.LIBRARIAN)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"
