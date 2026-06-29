from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.models import Book
from members.models import Member
from . import services
from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("book", "member").all()
    serializer_class = ReservationSerializer
    http_method_names = ["get", "post", "head", "options"]

    @action(detail=False, methods=["post"])
    def reserve(self, request):
        """Place a hold. Body: {"member_id": int, "book_id": int}."""
        try:
            member = Member.objects.get(pk=request.data["member_id"])
            book = Book.objects.get(pk=request.data["book_id"])
        except KeyError:
            return Response({"error": "member_id and book_id are required."}, status=400)
        except (Member.DoesNotExist, Book.DoesNotExist):
            return Response({"error": "Member or book not found."}, status=404)

        try:
            reservation = services.reserve(member, book)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=400)
        return Response(ReservationSerializer(reservation).data, status=201)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = Reservation.Status.CANCELLED
        reservation.save(update_fields=["status"])
        return Response(ReservationSerializer(reservation).data)
