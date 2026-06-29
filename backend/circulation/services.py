"""Business logic for the Circulation component.

Keeping checkout/checkin here (instead of in the view) keeps the view thin and
lets the Reservation and Reporting components reuse the same logic.
"""
from datetime import timedelta
from django.db import transaction
from django.utils import timezone

from catalog.models import BookCopy
from .models import Loan


class CirculationError(Exception):
    """Raised when a checkout or checkin breaks a library rule."""


@transaction.atomic
def checkout(member, copy, staff=None):
    if not member.can_borrow:
        raise CirculationError(
            "Member cannot borrow: account is not active or the loan limit is reached."
        )
    if copy.status != BookCopy.Status.AVAILABLE:
        raise CirculationError("This copy is not available for loan.")

    due_date = timezone.now().date() + timedelta(days=member.membership.loan_duration_days)
    loan = Loan.objects.create(copy=copy, member=member, staff=staff, due_date=due_date)
    copy.mark_on_loan()
    return loan


@transaction.atomic
def checkin(loan):
    if loan.status == Loan.Status.RETURNED:
        raise CirculationError("This loan has already been returned.")

    loan.return_date = timezone.now().date()
    loan.status = Loan.Status.RETURNED
    loan.save(update_fields=["return_date", "status"])
    loan.copy.mark_available()

    # Cross-component effects: fine if overdue, then notify the next reserver.
    from reporting.services import issue_overdue_fine
    from reservations.services import promote_next

    issue_overdue_fine(loan)
    promote_next(loan.copy.book)
    return loan
