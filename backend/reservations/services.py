"""Business logic for the Reservation component."""
from reporting.models import Notification
from .models import Reservation


def reserve(member, book):
    if not member.membership.can_reserve:
        raise ValueError("This membership type does not allow reservations.")

    existing = Reservation.objects.filter(
        book=book, member=member,
        status__in=[Reservation.Status.PENDING, Reservation.Status.READY],
    ).first()
    if existing:
        return existing

    position = Reservation.objects.filter(
        book=book, status=Reservation.Status.PENDING
    ).count() + 1
    return Reservation.objects.create(book=book, member=member, queue_position=position)


def promote_next(book):
    """When a copy is returned, move the first person in the queue to READY."""
    nxt = (
        Reservation.objects
        .filter(book=book, status=Reservation.Status.PENDING)
        .order_by("reservation_date")
        .first()
    )
    if nxt is None:
        return None
    nxt.status = Reservation.Status.READY
    nxt.save(update_fields=["status"])
    Notification.objects.create(
        member=nxt.member,
        message=f"'{book.title}' is now available for pickup.",
    )
    return nxt
