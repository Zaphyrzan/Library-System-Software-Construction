from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="copy.book.title", read_only=True)
    barcode = serializers.CharField(source="copy.barcode", read_only=True)
    member_name = serializers.CharField(source="member.name", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id", "copy", "barcode", "book_title", "member", "member_name",
            "staff", "loan_date", "due_date", "return_date", "status", "is_overdue",
        ]
        read_only_fields = ["loan_date", "due_date", "return_date", "status"]
