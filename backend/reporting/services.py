"""Fine calculation and report aggregation for the Reporting component."""
from decimal import Decimal
from django.utils import timezone

from .models import Fine

DAILY_FINE_RATE = Decimal("0.50")  # RM per day late


def calculate_overdue_amount(loan, on_date=None):
    """Return the fine owed for a loan, RM0.00 if not late."""
    on_date = on_date or timezone.now().date()
    end_date = loan.return_date or on_date
    days_late = (end_date - loan.due_date).days
    if days_late <= 0:
        return Decimal("0.00")
    return DAILY_FINE_RATE * days_late


def issue_overdue_fine(loan):
    """Create an overdue Fine for a loan if it was returned late."""
    amount = calculate_overdue_amount(loan)
    if amount > 0:
        return Fine.objects.create(loan=loan, amount=amount, reason=Fine.Reason.OVERDUE)
    return None
