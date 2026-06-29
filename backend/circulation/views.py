from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.models import BookCopy
from members.models import Member
from . import services
from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.select_related("copy__book", "member").all()
    serializer_class = LoanSerializer
    http_method_names = ["get", "post", "head", "options"]

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        """Issue a loan. Body: {"member_id": int, "copy_id": int}."""
        try:
            member = Member.objects.get(pk=request.data["member_id"])
            copy = BookCopy.objects.get(pk=request.data["copy_id"])
        except KeyError:
            return Response({"error": "member_id and copy_id are required."}, status=400)
        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=404)
        except BookCopy.DoesNotExist:
            return Response({"error": "Copy not found."}, status=404)

        try:
            loan = services.checkout(member, copy)
        except services.CirculationError as exc:
            return Response({"error": str(exc)}, status=400)
        return Response(LoanSerializer(loan).data, status=201)

    @action(detail=True, methods=["post"], url_path="return")
    def return_loan(self, request, pk=None):
        loan = self.get_object()
        try:
            services.checkin(loan)
        except services.CirculationError as exc:
            return Response({"error": str(exc)}, status=400)
        return Response(LoanSerializer(loan).data)
