from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.models import Book, BookCopy
from circulation.models import Loan
from members.models import Member
from reservations.models import Reservation
from .models import Fine, Notification
from .serializers import FineSerializer, NotificationSerializer


class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.select_related("loan__member", "loan__copy__book").all()
    serializer_class = FineSerializer

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        fine = self.get_object()
        fine.paid = True
        fine.payment_date = timezone.now().date()
        fine.save(update_fields=["paid", "payment_date"])
        return Response(FineSerializer(fine).data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.select_related("member").all()
    serializer_class = NotificationSerializer


class ReportViewSet(viewsets.ViewSet):
    """Aggregated reports for the dashboard."""

    def list(self, request):
        today = timezone.now().date()
        active_loans = Loan.objects.filter(status=Loan.Status.ACTIVE)
        summary = {
            "total_books": Book.objects.count(),
            "total_copies": BookCopy.objects.count(),
            "total_members": Member.objects.count(),
            "active_loans": active_loans.count(),
            "overdue_loans": active_loans.filter(due_date__lt=today).count(),
            "pending_reservations": Reservation.objects.filter(
                status=Reservation.Status.PENDING
            ).count(),
            "unpaid_fines": Fine.objects.filter(paid=False).aggregate(
                total=Sum("amount")
            )["total"] or 0,
        }
        return Response(summary)

    @action(detail=False, methods=["get"])
    def overdue(self, request):
        today = timezone.now().date()
        loans = Loan.objects.filter(
            status=Loan.Status.ACTIVE, due_date__lt=today
        ).select_related("member", "copy__book")
        data = [
            {
                "loan_id": loan.id,
                "member": loan.member.name,
                "book": loan.copy.book.title,
                "due_date": loan.due_date,
                "days_late": (today - loan.due_date).days,
            }
            for loan in loans
        ]
        return Response(data)

    @action(detail=False, methods=["get"])
    def popular(self, request):
        books = (
            Book.objects.annotate(loan_count=Count("copies__loans"))
            .order_by("-loan_count")[:5]
        )
        data = [{"title": b.title, "loans": b.loan_count} for b in books]
        return Response(data)
